from __future__ import annotations

from datetime import date

from sqlalchemy import BigInteger, Integer, Date, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from bot.infra.db import Base


class HoroscopeLog(Base):
    __tablename__ = "horoscope_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False)
    sign_code: Mapped[str] = mapped_column(String(32), nullable=False)

    __table_args__ = (
        Index("ix_horoscope_logs_user_day", "user_id", "day", unique=True),
        Index("ix_horoscope_logs_user_sign", "user_id", "sign_code"),
    )
