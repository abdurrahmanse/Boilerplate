from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    CLERK_WEBHOOK_SECRET: str = ""
    POSTHOG_KEY: str = ""
    POSTHOG_HOST: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

if not settings.DATABASE_URL:
    settings.DATABASE_URL = "sqlite+aiosqlite:///./dev.db"
elif settings.DATABASE_URL.startswith("postgres://") or settings.DATABASE_URL.startswith("postgresql://"):
    # Convert to asyncpg
    settings.DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    settings.DATABASE_URL = settings.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    # Strip incompatible parameters for asyncpg but ensure SSL is required for Neon
    if "?" in settings.DATABASE_URL:
        base_url = settings.DATABASE_URL.split("?")[0]
        settings.DATABASE_URL = base_url + "?ssl=require"
