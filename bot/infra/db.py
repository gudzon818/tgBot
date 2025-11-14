from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from bot.core.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database_url, echo=False)
SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False
)


async def init_db() -> None:
    # Импорт моделей, чтобы они были зарегистрированы в metadata
    from bot.models import feedback  # noqa: F401
    from bot.models import user  # noqa: F401
    from bot.models import daily_log  # noqa: F401
    from bot.models import quiz_progress  # noqa: F401
    from bot.models import quote_log  # noqa: F401
    from bot.models import horoscope_log  # noqa: F401
    from bot.models import mood_log  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()
