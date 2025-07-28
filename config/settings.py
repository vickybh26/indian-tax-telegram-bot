"""
Configuration settings for the Indian Tax Bot
"""

import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class Settings:
    """Configuration settings loaded from environment variables"""
    
    # API Keys
    telegram_token: str
    gemini_api_key: str
    
    # Bot Configuration
    bot_name: str = "Indian Tax Assistant Bot"
    bot_version: str = "1.0.0"
    max_message_length: int = 4096
    
    # Rate Limiting
    max_queries_per_hour: int = 10
    max_documents_per_day: int = 3
    
    # File Processing
    max_file_size_mb: int = 10
    temp_dir: str = "temp"
    
    # Gemini Configuration
    gemini_model: str = "gemini-2.5-pro"
    gemini_temperature: float = 0.3
    gemini_max_tokens: int = 2048
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "bot.log"
    
    def __init__(self):
        """Initialize settings from environment variables"""
        # Required environment variables
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
        # Optional environment variables with defaults
        self.bot_name = os.getenv("BOT_NAME", self.bot_name)
        self.bot_version = os.getenv("BOT_VERSION", self.bot_version)
        
        # Rate limiting settings
        self.max_queries_per_hour = int(os.getenv("MAX_QUERIES_PER_HOUR", self.max_queries_per_hour))
        self.max_documents_per_day = int(os.getenv("MAX_DOCUMENTS_PER_DAY", self.max_documents_per_day))
        
        # File processing settings
        self.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", self.max_file_size_mb))
        self.temp_dir = os.getenv("TEMP_DIR", self.temp_dir)
        
        # Gemini settings
        self.gemini_model = os.getenv("GEMINI_MODEL", self.gemini_model)
        self.gemini_temperature = float(os.getenv("GEMINI_TEMPERATURE", self.gemini_temperature))
        self.gemini_max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", self.gemini_max_tokens))
        
        # Logging settings
        self.log_level = os.getenv("LOG_LEVEL", self.log_level)
        self.log_file = os.getenv("LOG_FILE", self.log_file)
        
        # Create temp directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def validate(self) -> bool:
        """Validate that all required settings are present"""
        required_fields = [
            self.telegram_token,
            self.gemini_api_key
        ]
        
        return all(field.strip() for field in required_fields)
    
    def get_missing_settings(self) -> list[str]:
        """Get list of missing required settings"""
        missing = []
        
        if not self.telegram_token.strip():
            missing.append("TELEGRAM_BOT_TOKEN")
        
        if not self.gemini_api_key.strip():
            missing.append("GEMINI_API_KEY")
        
        return missing
    
    def __str__(self) -> str:
        """String representation of settings (without sensitive data)"""
        return f"""
Bot Settings:
- Name: {self.bot_name}
- Version: {self.bot_version}
- Telegram Token: {'✓ Set' if self.telegram_token else '✗ Missing'}
- Gemini API Key: {'✓ Set' if self.gemini_api_key else '✗ Missing'}
- Max Queries/Hour: {self.max_queries_per_hour}
- Max Documents/Day: {self.max_documents_per_day}
- Max File Size: {self.max_file_size_mb}MB
- Gemini Model: {self.gemini_model}
- Log Level: {self.log_level}
        """
