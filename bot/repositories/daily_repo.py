from __future__ import annotations

from datetime import date, datetime, timezone, timedelta
from typing import Literal

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.user import User
from bot.models.daily_log import DailyLog

Difficulty = Literal["easy", "medium", "hard", "gold"]

SCORES = {
    "easy": 1,
    "medium": 2,
    "hard": 3,
    "gold": 5,
}


class DailyRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def award_daily(self, user_id: int, username: str | None, category: str, difficulty: Difficulty) -> tuple[int, int]:
        today = date.today()
        # Upsert-like: get or create user
        res = await self.session.execute(select(User).where(User.user_id == user_id))
        u: User | None = res.scalar_one_or_none()
        if u is None:
            u = User(user_id=user_id, username=username)
            self.session.add(u)
            await self.session.flush()
        # Update streak
        if u.last_daily_on == today:
            # already counted today — do not double count
            pass
        else:
            if u.last_daily_on is not None and (today - u.last_daily_on) == timedelta(days=1):
                u.daily_streak = (u.daily_streak or 0) + 1
            else:
                u.daily_streak = 1
            u.last_daily_on = today
        # Score
        u.score = (u.score or 0) + SCORES.get(difficulty, 0)
        u.updated_at = datetime.now(timezone.utc)
        await self.session.flush()
        # Log
        log = DailyLog(
            user_id=user_id,
            day=today,
            category=category,
            difficulty=difficulty,
            status="done",
        )
        self.session.add(log)
        await self.session.commit()
        return u.score or 0, u.daily_streak or 0

    async def log_skip(self, user_id: int, category: str, difficulty: Difficulty) -> None:
        today = date.today()
        log = DailyLog(
            user_id=user_id,
            day=today,
            category=category,
            difficulty=difficulty,
            status="skipped",
        )
        self.session.add(log)
        await self.session.commit()

    async def has_today(self, user_id: int) -> bool:
        today = date.today()
        res = await self.session.execute(
            select(func.count()).select_from(DailyLog).where(
                (DailyLog.user_id == user_id) & (DailyLog.day == today)
            )
        )
        cnt = res.scalar() or 0
        return cnt > 0

    async def log_issued(self, user_id: int, category: str, difficulty: Difficulty) -> None:
        today = date.today()
        log = DailyLog(
            user_id=user_id,
            day=today,
            category=category,
            difficulty=difficulty,
            status="issued",
        )
        self.session.add(log)
        await self.session.commit()

    async def get_me(self, user_id: int) -> tuple[int, int]:
        res = await self.session.execute(select(User.score, User.daily_streak).where(User.user_id == user_id))
        row = res.first()
        if not row:
            return 0, 0
        return int(row[0] or 0), int(row[1] or 0)

    async def get_top(self, limit: int = 10) -> list[tuple[int, str | None, int]]:
        res = await self.session.execute(
            select(User.user_id, User.username, User.score).order_by(desc(User.score)).limit(limit)
        )
        return [(int(uid), uname, int(score or 0)) for uid, uname, score in res.all()]
