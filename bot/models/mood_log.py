from __future__ import annotations

from datetime import date

from sqlalchemy import BigInteger, Integer, Date, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from bot.infra.db import Base


class MoodLog(Base):
    __tablename__ = "mood_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False)
    mood_code: Mapped[str] = mapped_column(String(32), nullable=False)

    __table_args__ = (
        Index("ix_mood_logs_user_day", "user_id", "day", unique=True),
        Index("ix_mood_logs_user_mood", "user_id", "mood_code"),
    )
