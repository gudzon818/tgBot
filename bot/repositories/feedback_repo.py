from typing import Sequence

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.feedback import Feedback


class FeedbackRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, *, user_id: int, text: str) -> Feedback:
        fb = Feedback(user_id=user_id, text=text)
        self.session.add(fb)
        await self.session.commit()
        await self.session.refresh(fb)
        return fb

    async def last(self, limit: int = 10) -> Sequence[Feedback]:
        stmt = select(Feedback).order_by(desc(Feedback.id)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars())
