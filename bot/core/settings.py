from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/tgbot",
        alias="DATABASE_URL",
    )
    admin_id: int | None = Field(default=None, alias="ADMIN_ID")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )


settings = Settings()
