from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/tgbot",
        alias="DATABASE_URL",
    )
    admin_id: int | None = Field(default=None, alias="ADMIN_ID")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="bot.log", alias="LOG_FILE")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )


settings = Settings()
