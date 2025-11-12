import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from bot.infra.db import Base
from bot.models import feedback as _fb_mod  # noqa: F401 - register model
from bot.models import user as _user_mod  # noqa: F401 - register model
from bot.repositories.feedback_repo import FeedbackRepo
from bot.repositories.user_repo import UserRepo


@pytest.mark.asyncio
async def test_feedback_repo_add_and_last():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        repo = FeedbackRepo(session)
        await repo.add(user_id=123, text="hello world")
        items = await repo.last(limit=5)
        assert len(items) == 1
        assert items[0].text == "hello world"

    await engine.dispose()


@pytest.mark.asyncio
async def test_user_repo_get_set_lang():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        repo = UserRepo(session)
        u = await repo.get_or_create(777, "john")
        assert u.language_code == "ru"
        lang = await repo.get_lang(777)
        assert lang == "ru"
        await repo.set_lang(777, "en")
        lang2 = await repo.get_lang(777)
        assert lang2 == "en"

    await engine.dispose()
