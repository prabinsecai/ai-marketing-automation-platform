import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Marketing Automation & Campaign Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/marketing_platform"
    # Fallback to sqlite if postgres is not reachable or in test mode
    DATABASE_FALLBACK_SQLITE: bool = True
    SQLITE_DB_PATH: str = "sqlite:///./marketing_platform.db"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

    # AI Settings
    LLM_MODE: str = "mock"  # "mock" | "openai" | "anthropic"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-haiku-20241022"

    # AI Execution Config
    AI_TIMEOUT_SECONDS: int = 45
    AI_MAX_RETRIES: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
