from __future__ import annotations

from datetime import date

from sqlalchemy import BigInteger, Integer, Date, Index
from sqlalchemy.orm import Mapped, mapped_column

from bot.infra.db import Base


class QuoteLog(Base):
    __tablename__ = "quote_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False)
    quote_id: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        Index("ix_quote_logs_user_day", "user_id", "day", unique=True),
        Index("ix_quote_logs_user_quote", "user_id", "quote_id"),
    )
