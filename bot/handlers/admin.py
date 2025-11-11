from aiogram import Router, types
from aiogram.filters import Command
from bot.filters.admin import IsAdmin
from bot.core.settings import settings
from bot.infra.db import SessionLocal
from sqlalchemy import text
import redis.asyncio as aioredis
from bot.services.runtime import uptime_seconds

router = Router()


@router.message(Command("admin"), IsAdmin())
async def cmd_admin(message: types.Message) -> None:
    await message.answer("Админ-панель: у вас есть доступ к административным командам.")


@router.message(Command("stats"), IsAdmin())
async def cmd_stats(message: types.Message) -> None:
    # Redis ping
    redis_ok = False
    try:
        r = aioredis.from_url(settings.redis_url, decode_responses=True)
        pong = await r.ping()
        await r.close()
        redis_ok = bool(pong)
    except Exception:
        redis_ok = False

    # DB ping
    db_ok = False
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        db_ok = False

    text_msg = (
        "Stats:\n"
        f"Uptime: {uptime_seconds()}s\n"
        f"Redis: {'OK' if redis_ok else 'FAIL'}\n"
        f"DB: {'OK' if db_ok else 'FAIL'}\n"
        f"Log level: {settings.log_level}\n"
    )
    await message.answer(text_msg)
