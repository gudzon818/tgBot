from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, Integer, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from bot.infra.db import Base


class QuizProgress(Base):
    __tablename__ = "quiz_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, nullable=False)
    last_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        Index("ix_quiz_progress_user_question", "user_id", "question_id", unique=True),
    )
