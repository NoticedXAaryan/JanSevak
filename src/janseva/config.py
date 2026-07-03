"""
Central configuration module.
Reads all settings from environment variables (.env file).
"""
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- Telegram ---
    telegram_bot_token: str = Field(..., description="Telegram bot token from BotFather")

    # --- Database ---
    database_url: str = Field(
        "postgresql+asyncpg://janseva:janseva_dev@localhost:5432/janseva",
        description="Async PostgreSQL connection string",
    )
    database_url_sync: str = Field(
        "postgresql://janseva:janseva_dev@localhost:5432/janseva",
        description="Sync PostgreSQL connection string (for Alembic)",
    )

    # --- Redis ---
    redis_url: str = Field("redis://localhost:6379/0")

    # --- LLM ---
    google_api_key: str = Field("", description="Google Gemini API key")
    openrouter_api_key: str = Field("", description="OpenRouter API key")
    groq_api_key: str = Field("", description="Groq API key")
    llm_provider: str = Field(
        "gemini",
        description="LLM provider: 'gemini', 'ollama', or 'openrouter'",
    )
    llm_model: str = Field("gemini-2.0-flash", description="LLM model name")
    ollama_base_url: str = Field("http://localhost:11434")
    embedding_provider: str = Field(
        "gemini",
        description="Embedding provider: 'gemini' or 'ollama'. OpenRouter is chat-only here.",
    )
    embedding_model: str = Field(
        "",
        description="Embedding model override. Defaults depend on EMBEDDING_PROVIDER.",
    )

    # --- Security ---
    admin_jwt_secret: str = Field("change-me", description="JWT secret for admin auth")
    report_encryption_key: str = Field("change-me", description="Fernet key for report encryption")

    # --- Admin ---
    admin_username: str = Field("admin")
    admin_password: str = Field("change-me")

    # --- Twilio (WhatsApp) Settings ---
    twilio_account_sid: str = Field("", description="Twilio Account SID")
    twilio_auth_token: str = Field("", description="Twilio Auth Token")
    twilio_whatsapp_number: str = Field("", description="Twilio WhatsApp number (e.g., whatsapp:+1234567890)")

    # --- App ---
    env: str = Field("development")
    log_level: str = Field("DEBUG")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton instance — import this everywhere
settings = Settings()
