from __future__ import annotations

import random
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.quote_log import QuoteLog


class QuoteRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_today(self, user_id: int, today: date) -> int | None:
        """Вернуть id цитаты, выданной сегодня пользователю (если есть)."""
        res = await self.session.execute(
            select(QuoteLog.quote_id).where(
                QuoteLog.user_id == user_id,
                QuoteLog.day == today,
            )
        )
        row = res.first()
        return int(row[0]) if row else None

    async def issue_new_for_today(self, user_id: int, today: date, total_quotes: int) -> int | None:
        """Выдать новую цитату на сегодня, избегая повторов.

        Возвращает id цитаты или None, если все цитаты уже были показаны.
        """
        # Сначала проверим, не выдана ли уже цитата сегодня
        existing = await self.get_today(user_id, today)
        if existing is not None:
            return existing

        # Получим все уже показанные цитаты
        res = await self.session.execute(
            select(QuoteLog.quote_id).where(QuoteLog.user_id == user_id)
        )
        used_ids = {int(row[0]) for row in res}
        candidates = [qid for qid in range(1, total_quotes + 1) if qid not in used_ids]
        if not candidates:
            return None

        qid = random.choice(candidates)
        log = QuoteLog(user_id=user_id, day=today, quote_id=qid)
        self.session.add(log)
        await self.session.commit()
        return qid
