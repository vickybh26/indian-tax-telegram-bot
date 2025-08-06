"""
Response formatting utilities for structured bot responses
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ResponseFormatter:
    """Formats responses for better readability and structure"""
    
    def __init__(self):
        self.disclaimer_text = """
⚠️ Disclaimer: This information is for general guidance only and should not be considered as professional tax advice. Tax laws are subject to change and individual circumstances may vary. Always consult a qualified Chartered Accountant or tax advisor for personalized advice.
        """
    
    def format_tax_response(self, response_data: Dict[str, Any]) -> str:
        """Format tax query response for Telegram"""
        try:
            answer = response_data.get('answer', 'No answer available')
            confidence = response_data.get('confidence', 0.0)
            relevant_sections = response_data.get('relevant_sections', [])
            official_links = response_data.get('official_links', [])
            
            # Clean the answer text to avoid parsing issues
            answer = self._clean_text_for_telegram(answer)
            
            # Truncate answer if too long (leave room for other content)
            max_answer_length = 3500  # Leave room for header, links, disclaimer
            if len(answer) > max_answer_length:
                answer = answer[:max_answer_length] + "... (truncated for length)"
            
            # Build formatted response with safe formatting - NO MARKDOWN
            formatted_response = "💰 TAX INFORMATION\n\n"
            formatted_response += f"{answer}\n\n"
            
            # Add relevant sections if available (limit to save space)
            if relevant_sections:
                formatted_response += "📋 RELEVANT SECTIONS:\n"
                for section in relevant_sections[:3]:  # Limit to 3 sections
                    clean_section = self._clean_text_for_telegram(section)
                    if len(clean_section) > 100:
                        clean_section = clean_section[:100] + "..."
                    formatted_response += f"• {clean_section}\n"
                formatted_response += "\n"
            
            # Add official links if available
            if official_links:
                formatted_response += "🔗 OFFICIAL RESOURCES:\n"
                for link in official_links[:2]:  # Limit to 2 links to save space
                    formatted_response += f"• {link}\n"
                formatted_response += "\n"
            
            # Add confidence indicator
            confidence_emoji = self._get_confidence_emoji(confidence)
            formatted_response += f"{confidence_emoji} CONFIDENCE: {confidence:.0%}\n\n"
            
            # Add shorter disclaimer
            short_disclaimer = "⚠️ General information only. Consult a qualified tax advisor for personalized advice."
            formatted_response += short_disclaimer
            
            # Final safety check - if still too long, truncate
            if len(formatted_response) > 4000:
                formatted_response = formatted_response[:3900] + "...\n\n" + short_disclaimer
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error formatting tax response: {e}")
            return self._get_error_response()
    
    def format_document_analysis(self, analysis_data: Dict[str, Any], filename: str) -> str:
        """Format document analysis response"""
        try:
            analysis = analysis_data.get('analysis', 'No analysis available')
            status = analysis_data.get('status', 'unknown')
            
            # Clean analysis text
            analysis = self._clean_text_for_telegram(analysis)
            
            if status == 'error':
                return f"❌ DOCUMENT ANALYSIS FAILED\n\n{analysis}\n\n{self.disclaimer_text}"
            
            formatted_response = f"📄 DOCUMENT ANALYSIS: {filename}\n\n"
            formatted_response += f"{analysis}\n\n"
            
            # Add processing timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_response += f"🕒 ANALYZED ON: {timestamp}\n\n"
            
            # Add disclaimer
            disclaimer = self._clean_text_for_telegram(self.disclaimer_text)
            formatted_response += disclaimer
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error formatting document analysis: {e}")
            return self._get_error_response()
    
    def format_error_response(self, error_message: str, query_type: str = "query") -> str:
        """Format error response"""
        clean_message = self._clean_text_for_telegram(error_message)
        
        return f"""❌ ERROR PROCESSING {query_type.upper()}

{clean_message}

WHAT YOU CAN TRY:
• Rephrase your question
• Check if your document is a valid PDF
• Try again in a few moments
• Use /help for guidance

If the problem persists, please contact support.

{self.disclaimer_text}"""
    
    def format_rate_limit_response(self, limit_type: str) -> str:
        """Format rate limit exceeded response"""
        if limit_type == "text_query":
            return """⏰ QUERY LIMIT REACHED

You've reached the hourly limit for text queries (10 per hour).

WHAT YOU CAN DO:
• Wait for the next hour to reset
• Consider consolidating multiple questions into one
• Use /help for guidance on effective queries

Thank you for your understanding! 🙏"""
        elif limit_type == "document_analysis":
            return """📄 DOCUMENT ANALYSIS LIMIT REACHED

You've reached the daily limit for document analysis (3 per day).

WHAT YOU CAN DO:
• Wait for tomorrow to reset
• Combine multiple documents if possible
• Ask text-based questions about specific tax topics

Thank you for your understanding! 🙏"""
        else:
            return "⏰ You've reached the usage limit. Please try again later."
    
    def format_welcome_features(self) -> List[str]:
        """Get formatted list of bot features"""
        return [
            "💵 Income tax calculations and planning",
            "🏛️ Deduction eligibility (80C, 80D, HRA, etc.)",
            "📅 Filing deadlines and requirements",
            "📊 Tax slab information for current FY",
            "📄 PDF document analysis (Form 16, ITR, etc.)",
            "🔍 GST basics and compliance queries",
            "💡 Tax-saving investment guidance",
            "📋 ITR form selection help"
        ]
    
    def format_quick_help_commands(self) -> str:
        """Format quick help commands"""
        return """QUICK COMMANDS:
/start - Start the bot
/help - Detailed help and examples
/about - About this bot

EXAMPLE QUESTIONS:
• "What are current tax slabs?"
• "How much can I save under 80C?"
• "When is ITR filing deadline?"
• "Calculate my HRA exemption"
        """
    
    def _get_confidence_emoji(self, confidence: float) -> str:
        """Get emoji based on confidence level"""
        if confidence >= 0.9:
            return "🟢"
        elif confidence >= 0.7:
            return "🟡"
        elif confidence >= 0.5:
            return "🟠"
        else:
            return "🔴"
    
    def _clean_text_for_telegram(self, text: str) -> str:
        """Clean text to avoid Telegram parsing errors"""
        if not text:
            return ""
        
        # Remove ALL markdown formatting that causes issues
        cleaned = text.replace("**", "").replace("*", "").replace("_", "").replace("`", "")
        cleaned = cleaned.replace("__", "").replace("~~", "").replace("```", "")
        
        # Remove problematic characters that cause parsing errors
        problematic_chars = ['[', ']', '(', ')', '{', '}', '|', '\\', '<', '>']
        for char in problematic_chars:
            if char in '()':  # Keep parentheses as they're useful in tax info
                continue
            cleaned = cleaned.replace(char, "")
        
        # Normalize quotes
        cleaned = cleaned.replace('"', '"').replace('"', '"').replace("'", "'").replace("'", "'")
        
        # Remove excessive whitespace and newlines
        while "  " in cleaned:
            cleaned = cleaned.replace("  ", " ")
        while "\n\n\n" in cleaned:
            cleaned = cleaned.replace("\n\n\n", "\n\n")
        
        # Remove any remaining control characters
        cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\n\r\t')
        
        return cleaned.strip()
    
    def _get_error_response(self) -> str:
        """Get generic error response"""
        return f"""❌ PROCESSING ERROR

Sorry, I encountered an error while processing your request. Please try again later.

If the problem persists, please contact support.

{self.disclaimer_text}"""
    
    def format_tax_calculation_example(self, income: int, regime: str = "new") -> str:
        """Format tax calculation example"""
        try:
            if regime == "new":
                # New tax regime calculation
                tax = 0
                if income > 300000:
                    tax += min(income - 300000, 300000) * 0.05
                if income > 600000:
                    tax += min(income - 600000, 300000) * 0.10
                if income > 900000:
                    tax += min(income - 900000, 300000) * 0.15
                if income > 1200000:
                    tax += min(income - 1200000, 300000) * 0.20
                if income > 1500000:
                    tax += (income - 1500000) * 0.30
            else:
                # Old tax regime calculation
                tax = 0
                if income > 250000:
                    tax += min(income - 250000, 250000) * 0.05
                if income > 500000:
                    tax += min(income - 500000, 500000) * 0.20
                if income > 1000000:
                    tax += (income - 1000000) * 0.30
            
            # Add cess
            total_tax = tax * 1.04  # 4% cess
            
            return f"""TAX CALCULATION EXAMPLE ({regime.upper()} REGIME)

Annual Income: ₹{income:,}
Income Tax: ₹{tax:,.0f}
Health & Education Cess (4%): ₹{tax * 0.04:,.0f}
TOTAL TAX: ₹{total_tax:,.0f}"""
            
        except Exception as e:
            logger.error(f"Error formatting tax calculation: {e}")
            return "Unable to calculate tax at this time."