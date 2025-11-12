from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.user import User


class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_or_create(self, user_id: int, username: str | None, default_lang: str = "ru") -> User:
        res = await self.session.execute(select(User).where(User.user_id == user_id))
        obj = res.scalar_one_or_none()
        if obj is None:
            obj = User(user_id=user_id, username=username, language_code=default_lang)
            self.session.add(obj)
            await self.session.flush()
        else:
            # touch username/updated_at
            obj.username = username
            obj.updated_at = datetime.now(timezone.utc)
            await self.session.flush()
        return obj

    async def get_lang(self, user_id: int, default_lang: str = "ru") -> str:
        res = await self.session.execute(select(User.language_code).where(User.user_id == user_id))
        lang = res.scalar_one_or_none()
        return lang or default_lang

    async def set_lang(self, user_id: int, lang: str) -> None:
        await self.session.execute(
            update(User)
            .where(User.user_id == user_id)
            .values(language_code=lang, updated_at=datetime.now(timezone.utc))
        )
        await self.session.commit()
