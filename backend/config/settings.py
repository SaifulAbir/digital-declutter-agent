"""
Configuration settings for the Digital Declutter Agent API.

This module uses Pydantic Settings to manage environment variables and
application configuration in a type-safe manner.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    """

    # =============================================================================
    # DATABASE CONFIGURATION
    # =============================================================================
    DATABASE_URL: str = "sqlite:///./declutter.db"

    # =============================================================================
    # GOOGLE OAUTH CONFIGURATION
    # =============================================================================
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/callback"

    # =============================================================================
    # JWT (JSON Web Token) CONFIGURATION
    # =============================================================================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # =============================================================================
    # AI SERVICE CONFIGURATION
    # =============================================================================
    GEMINI_API_KEY: str

    # =============================================================================
    # CORS (Cross-Origin Resource Sharing) CONFIGURATION
    # =============================================================================
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # =============================================================================
    # GOOGLE API SCOPES
    # =============================================================================
    GMAIL_SCOPES: List[str] = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ]

    DRIVE_SCOPES: List[str] = [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.file",
    ]

    class Config:
        """
        Pydantic Settings configuration.

        env_file: Specifies the .env file to load environment variables from.
        """

        env_file = ".env"


# Global settings instance
settings = Settings()
