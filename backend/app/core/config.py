from typing import List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Medical Report Assistant API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:LIKITH2233@localhost:5432/medical_report"

    # JWT Authentication Security
    SECRET_KEY: str = "super_secret_jwt_key_change_in_production_32bytes_min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS Allowed Origins
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    # Gemini AI Configuration
    GEMINI_API_KEY: Optional[str] = None          # Set in .env — never hardcode
    GEMINI_MODEL: str = "gemini-2.0-flash"        # Model to use for summary generation
    GEMINI_TIMEOUT_SECONDS: int = 10              # Per-request HTTP timeout
    GEMINI_MAX_RETRIES: int = 2                   # Retry attempts on transient errors

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()



print("=" * 100)
print("DATABASE_URL:", settings.DATABASE_URL)
print("=" * 100)
