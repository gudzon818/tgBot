from __future__ import annotations

import random
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.quiz_progress import QuizProgress


class QuizRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def pick_next_question_id(self, user_id: int, total_questions: int) -> int | None:
        """Вернуть id вопроса, на который пользователь ещё не ответил правильно.

        Если таких вопросов нет — вернуть None.
        """
        res = await self.session.execute(
            select(QuizProgress.question_id).where(
                QuizProgress.user_id == user_id,
                QuizProgress.last_correct.is_(True),
            )
        )
        solved_ids = {row[0] for row in res}
        candidates = [qid for qid in range(1, total_questions + 1) if qid not in solved_ids]
        if not candidates:
            return None
        return random.choice(candidates)

    async def mark_answer(self, user_id: int, question_id: int, is_correct: bool) -> None:
        now = datetime.now(timezone.utc)
        res = await self.session.execute(
            select(QuizProgress).where(
                QuizProgress.user_id == user_id,
                QuizProgress.question_id == question_id,
            )
        )
        row = res.scalar_one_or_none()
        if row is None:
            row = QuizProgress(
                user_id=user_id,
                question_id=question_id,
                last_correct=is_correct,
                attempts=1,
                last_answered_at=now,
            )
            self.session.add(row)
        else:
            row.last_correct = is_correct
            row.attempts += 1
            row.last_answered_at = now
        await self.session.commit()


    async def get_solved_count(self, user_id: int) -> int:
        """Сколько вопросов пользователь уже решил правильно хотя бы раз."""
        res = await self.session.execute(
            select(QuizProgress).where(
                QuizProgress.user_id == user_id,
                QuizProgress.last_correct.is_(True),
            )
        )
        rows = res.scalars().all()
        return len(rows)
