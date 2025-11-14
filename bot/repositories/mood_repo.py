from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.mood_log import MoodLog


class MoodRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def log_today(self, user_id: int, today: date, mood_code: str) -> None:
        # один лог в день: перезаписываем, если уже был
        res = await self.session.execute(
            select(MoodLog).where(MoodLog.user_id == user_id, MoodLog.day == today)
        )
        row = res.scalar_one_or_none()
        if row is None:
            row = MoodLog(user_id=user_id, day=today, mood_code=mood_code)
            self.session.add(row)
        else:
            row.mood_code = mood_code
        await self.session.commit()

    async def get_stats(self, user_id: int) -> dict[str, int]:
        res = await self.session.execute(
            select(MoodLog.mood_code).where(MoodLog.user_id == user_id)
        )
        counts: dict[str, int] = {}
        for (code,) in res.all():
            counts[code] = counts.get(code, 0) + 1
        return counts

    async def get_total_days(self, user_id: int) -> int:
        res = await self.session.execute(
            select(MoodLog.day).where(MoodLog.user_id == user_id)
        )
        days = {day for (day,) in res.all()}
        return len(days)
