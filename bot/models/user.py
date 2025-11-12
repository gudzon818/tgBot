from datetime import datetime, timezone, date
from sqlalchemy import BigInteger, DateTime, String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from bot.infra.db import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    language_code: Mapped[str] = mapped_column(String(8), nullable=False, default="ru")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    # Gamification
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    daily_streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_daily_on: Mapped[date | None] = mapped_column(Date, nullable=True)
