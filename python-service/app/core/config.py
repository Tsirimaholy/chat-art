"""
Configuration management for FAQ Finance Chatbot

This module contains all configuration settings and environment variables
for the FAQ Finance Chatbot service.
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Service configuration
    service_name: str = "FAQ Finance Chatbot"
    service_version: str = "1.0.0"
    debug: bool = False
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8001
    
    # CORS settings
    cors_origins: List[str] = ["http://localhost:3000"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # FAQ matching configuration
    similarity_threshold: float = 0.3
    max_message_length: int = 1000
    
    # File paths
    data_dir: str = "data"
    faq_file: str = "faq.json"
    
    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @property
    def faq_file_path(self) -> str:
        """Get the full path to the FAQ file"""
        return os.path.join(self.data_dir, self.faq_file)
    
    class Config:
        env_prefix = "FAQ_"
        case_sensitive = False
        env_file = ".env"


# Global settings instance
settings = Settings()