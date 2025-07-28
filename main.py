#!/usr/bin/env python3
"""
Main entry point for the Indian Income Tax Telegram Bot
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

from bot.telegram_bot import TaxBot
from config.settings import Settings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the Telegram bot"""
    try:
        # Initialize settings
        settings = Settings()
        
        # Validate required environment variables
        if not settings.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        logger.info("Starting Indian Income Tax Telegram Bot...")
        
        # Initialize and start the bot
        bot = TaxBot(settings)
        await bot.start()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
