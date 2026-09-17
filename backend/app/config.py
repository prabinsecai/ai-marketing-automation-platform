import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Marketing Automation & Campaign Intelligence Platform"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/marketing_platform"
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

    # Phase 2: Local n8n Integration & Execution Config
    N8N_BASE_URL: str = "http://localhost:5678"
    N8N_WEBHOOK_CAMPAIGN_EXECUTE: str = "/webhook/campaign-execute"
    N8N_WEBHOOK_LEAD_FOLLOWUP: str = "/webhook/lead-followup"
    N8N_WEBHOOK_MOCK_EMAIL: str = "/webhook/mock-email"
    N8N_WEBHOOK_MOCK_CRM: str = "/webhook/mock-crm"
    N8N_WEBHOOK_SECRET: str = "marketing-automation-n8n-secret"
    MAX_EXECUTION_RETRIES: int = 3
    N8N_TIMEOUT_SECONDS: int = 30
    BACKEND_PUBLIC_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
