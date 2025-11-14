from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.horoscope_log import HoroscopeLog


class HoroscopeRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_today(self, user_id: int, today: date) -> str | None:
        res = await self.session.execute(
            select(HoroscopeLog.sign_code).where(
                HoroscopeLog.user_id == user_id,
                HoroscopeLog.day == today,
            )
        )
        row = res.first()
        return str(row[0]) if row else None

    async def log_today(self, user_id: int, today: date, sign_code: str) -> None:
        row = HoroscopeLog(user_id=user_id, day=today, sign_code=sign_code)
        self.session.add(row)
        await self.session.commit()
