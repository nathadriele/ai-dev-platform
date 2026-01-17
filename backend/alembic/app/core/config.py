from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "AI-Assisted Developer Productivity Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./ai_dev_platform.db",
        description="Database connection URL"
    )

    # Authentication
    secret_key: str = Field(
        ...,
        description="Secret key for JWT token encoding"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        description="Allowed CORS origins"
    )

    # External Services
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    github_token: str = ""

    # MCP
    mcp_github_endpoint: str = ""
    mcp_filesystem_endpoint: str = ""
    mcp_database_endpoint: str = ""

    # CI/CD
    github_webhook_secret: str = ""

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Rate Limiting
    rate_limit_per_minute: int = 100

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @validator("database_url")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
