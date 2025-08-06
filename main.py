#!/usr/bin/env python3
"""
Main entry point for the Indian Income Tax Telegram Bot
"""

import asyncio
import logging
import os
import signal
import sys
from dotenv import load_dotenv

from bot.telegram_bot import TaxBot
from config.settings import Settings

# Load environment variables
load_dotenv()

# Configure logging for Railway deployment
log_handlers = [logging.StreamHandler(sys.stdout)]

# Only add file handler if we can write to disk (not always possible on Railway)
try:
    log_handlers.append(logging.FileHandler('bot.log'))
except (PermissionError, OSError):
    pass  # Skip file logging if filesystem is restricted

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=log_handlers
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the Telegram bot"""
    bot = None
    try:
        logger.info("Initializing Indian Income Tax Telegram Bot...")
        
        # Initialize settings
        settings = Settings()
        
        # Validate required environment variables
        if not settings.telegram_token:
            logger.error("TELEGRAM_BOT_TOKEN environment variable is missing")
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        if not settings.gemini_api_key:
            logger.error("GEMINI_API_KEY environment variable is missing")
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        logger.info("Environment variables validated successfully")
        logger.info("Starting Telegram bot...")
        
        # Initialize and start the bot
        bot = TaxBot(settings)
        
        # Set up signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down gracefully...")
            if bot:
                asyncio.create_task(bot.stop())
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start the bot
        await bot.start()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error("Full traceback:")
        logger.error(traceback.format_exc())
        
        if bot:
            try:
                await bot.stop()
            except:
                pass
        
        # Exit with error code for Railway to detect failure
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
