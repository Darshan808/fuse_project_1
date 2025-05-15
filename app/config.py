"""
Configuration module that loads settings from environment variables
using Pydantic's BaseSettings.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API settings
    APP_NAME: str = "Currency Converter API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # External API
    EXCHANGE_API_KEY: str
    EXCHANGE_API_URL: str

    # Redis settings (for caching)
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    CACHE_TTL: int = 3600  # Cache TTL in seconds

    # CORS settings
    CORS_ORIGINS: str = "*"

    class Config:
        """Pydantic config for loading .env file."""

        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Return cached settings instance to avoid loading .env file
    multiple times.
    """
    return Settings()
