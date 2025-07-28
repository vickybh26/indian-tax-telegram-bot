"""
Telegram Bot implementation for Indian Income Tax queries
"""

import asyncio
import logging
import os
from typing import Optional
from telegram import Update, Document
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from services.gemini_service import GeminiService
from services.document_processor import DocumentProcessor
from utils.response_formatter import ResponseFormatter
from utils.rate_limiter import RateLimiter
from config.settings import Settings

logger = logging.getLogger(__name__)

class TaxBot:
    """Main Telegram Bot class for handling tax queries"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.gemini_service = GeminiService(settings.gemini_api_key)
        self.document_processor = DocumentProcessor()
        self.response_formatter = ResponseFormatter()
        self.rate_limiter = RateLimiter()
        
        # Initialize Telegram application
        self.application = Application.builder().token(settings.telegram_token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("about", self.about_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_query))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if not update.message:
            return
            
        user = update.effective_user
        user_name = user.first_name if user else "there"
        welcome_message = f"""
🇮🇳 **Welcome to Indian Income Tax Assistant Bot!** 🇮🇳

Hello {user_name}! I'm here to help you with Indian income tax queries using AI-powered responses.

**What I can help you with:**
• Income tax calculations
• Deduction eligibility (80C, 80D, etc.)
• Filing requirements and deadlines
• Tax planning strategies
• Basic GST queries
• Document analysis for tax-related PDFs

**How to use:**
• Simply send me your tax-related questions
• Upload tax documents (PDF) for analysis
• Use /help for more information

⚠️ **Important Disclaimer:**
This bot provides general information only and should not be considered as professional tax advice. Always consult a qualified tax professional for specific situations.

Ready to help! What's your tax question? 💰
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if not update.message:
            return
        help_message = """
📚 **How to use the Indian Tax Assistant Bot:**

**Text Queries:**
• Ask about income tax rates and slabs
• Inquire about deductions (80C, 80D, HRA, etc.)
• Get filing deadlines and requirements
• Ask about tax planning strategies
• Basic GST information

**Document Analysis:**
• Upload PDF documents (Form 16, IT returns, etc.)
• Get analysis and insights from your tax documents

**Example Questions:**
• "What are the income tax slabs for FY 2023-24?"
• "Am I eligible for 80C deduction?"
• "When is the ITR filing deadline?"
• "How to calculate HRA exemption?"

**Commands:**
/start - Start the bot
/help - Show this help message
/about - About this bot

**Rate Limits:**
• Max 10 queries per hour per user
• Document analysis: Max 3 per day per user

Need help? Just ask your question! 🤝
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        if not update.message:
            return
        about_message = """
🤖 **About Indian Tax Assistant Bot**

**Powered by:**
• Google Gemini AI for intelligent responses
• Updated Indian tax law knowledge base
• Document processing capabilities

**Features:**
• Real-time tax query responses
• PDF document analysis
• Structured answers with official links
• Rate limiting for optimal performance

**Data Sources:**
• Income Tax Act, 1961
• Latest Budget announcements
• CBDT notifications
• Official government resources

**Version:** 1.0.0
**Last Updated:** July 2025

⚠️ **Disclaimer:** This bot provides general information only. Always consult qualified tax professionals for personalized advice.

**Feedback:** If you find any issues or have suggestions, please contact the developer.
        """
        
        await update.message.reply_text(about_message, parse_mode='Markdown')
    
    async def handle_text_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text-based tax queries"""
        if not update.effective_user or not update.message or not update.message.text:
            return
            
        user_id = update.effective_user.id
        query = update.message.text
        
        try:
            # Check rate limiting
            if not self.rate_limiter.check_rate_limit(user_id, 'text_query'):
                await update.message.reply_text(
                    "⏰ You've reached the hourly query limit. Please try again later."
                )
                return
            
            # Show typing indicator
            if update.effective_chat:
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Process query with Gemini
            response = await self.gemini_service.process_tax_query(query)
            
            # Format response
            formatted_response = self.response_formatter.format_tax_response(response)
            
            # Send response
            await update.message.reply_text(formatted_response, parse_mode='Markdown')
            
            logger.info(f"Processed text query for user {user_id}: {query[:50]}...")
            
        except Exception as e:
            logger.error(f"Error processing text query: {e}")
            await update.message.reply_text(
                "❌ Sorry, I encountered an error processing your query. Please try again later or rephrase your question."
            )
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads for analysis"""
        if not update.effective_user or not update.message or not update.message.document:
            return
            
        user_id = update.effective_user.id
        document = update.message.document
        
        try:
            # Check rate limiting for document analysis
            if not self.rate_limiter.check_rate_limit(user_id, 'document_analysis'):
                await update.message.reply_text(
                    "📄 You've reached the daily document analysis limit. Please try again tomorrow."
                )
                return
            
            # Check file type
            if not document.file_name or not document.file_name.lower().endswith('.pdf'):
                await update.message.reply_text(
                    "📄 Please upload PDF files only for document analysis."
                )
                return
            
            # Check file size (max 10MB)
            if document.file_size and document.file_size > 10 * 1024 * 1024:
                await update.message.reply_text(
                    "📄 File size too large. Please upload files smaller than 10MB."
                )
                return
            
            await update.message.reply_text("📄 Processing your document... This may take a moment.")
            
            # Show typing indicator
            if update.effective_chat:
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Download and process document
            file = await context.bot.get_file(document.file_id)
            file_path = f"temp/{document.file_id}.pdf"
            
            # Create temp directory if it doesn't exist
            os.makedirs("temp", exist_ok=True)
            
            # Download file
            await file.download_to_drive(file_path)
            
            # Process document
            document_text = self.document_processor.extract_text_from_pdf(file_path)
            
            # Analyze with Gemini
            analysis = await self.gemini_service.analyze_tax_document(document_text, document.file_name or "document.pdf")
            
            # Format response
            formatted_response = self.response_formatter.format_document_analysis(analysis, document.file_name or "document.pdf")
            
            # Send response
            await update.message.reply_text(formatted_response, parse_mode='Markdown')
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            
            logger.info(f"Processed document for user {user_id}: {document.file_name}")
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            await update.message.reply_text(
                "❌ Sorry, I couldn't process your document. Please ensure it's a valid PDF and try again."
            )
            
            # Clean up on error
            try:
                if 'file_path' in locals() and os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup errors
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.message:
            await update.message.reply_text(
                "❌ An unexpected error occurred. Please try again later."
            )
    
    async def start(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        # Keep the bot running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
            await self.application.stop()
