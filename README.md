# Indian Income Tax Telegram Bot

A sophisticated Telegram bot that provides AI-powered Indian income tax guidance using Google Gemini AI.

## Features

- **Intelligent Tax Advice**: Powered by Google Gemini AI for accurate responses
- **PDF Document Analysis**: Upload and analyze tax documents (Form 16, ITR, etc.)
- **Comprehensive Tax Knowledge**: Current Indian tax laws, slabs, and deductions
- **Rate Limiting**: Prevents abuse with configurable usage limits
- **Structured Responses**: Confidence levels, relevant sections, and official links

## Quick Start

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `GEMINI_API_KEY`: Your Google Gemini API key
4. Run: `python main.py`

## Environment Variables

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

## Deployment

This bot is ready for deployment on:
- Railway.app (recommended for small scale)
- Heroku
- Google Cloud Run
- AWS Lambda
- Any Python hosting service

## Usage

Users can:
- Ask tax questions in natural language
- Upload PDF documents for analysis
- Get structured responses with confidence levels
- Access official tax resources and links

## Commands

- `/start` - Welcome message and bot overview
- `/help` - Detailed usage instructions  
- `/about` - Information about the bot

## Rate Limits

- Text queries: 10 per hour per user
- Document analysis: 3 per day per user

## Tech Stack

- Python 3.11+
- python-telegram-bot
- Google Gemini AI
- PyPDF2 for document processing
- Pydantic for data validation

## License

MIT License