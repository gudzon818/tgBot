from aiogram import Router, types
from aiogram.filters import Command
from bot.filters.admin import IsAdmin
from bot.core.settings import settings
from bot.infra.db import SessionLocal
from sqlalchemy import text, select, func
import redis.asyncio as aioredis
from bot.services.runtime import uptime_seconds
from bot.models.feedback import Feedback
import os
import aiogram

try:
    import resource  # type: ignore
except Exception:  # pragma: no cover
    resource = None  # type: ignore

from bot.services.metrics import snapshot as metrics_snapshot
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
    fb_count = None
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
            db_ok = True
            res = await session.execute(select(func.count()).select_from(Feedback))
            fb_count = res.scalar() or 0
    except Exception:
        db_ok = False

    text_msg = (
        "Stats:\n"
        f"Uptime: {uptime_seconds()}s\n"
        f"Redis: {'OK' if redis_ok else 'FAIL'}\n"
        f"DB: {'OK' if db_ok else 'FAIL'}\n"
        f"Log level: {settings.log_level}\n"
        f"Mode: {'webhook' if settings.webhook_mode else 'polling'}\n"
        f"Version: {os.environ.get('APP_VERSION','dev')}\n"
        f"Git SHA: {os.environ.get('GIT_SHA','unknown')}\n"
        f"Aiogram: {getattr(aiogram, '__version__', 'unknown')}\n"
        f"RAM (RSS): {_calc_rss_mb()} MB\n"
        f"CPU load (1/5/15m): {_load_avg()}\n"
        f"Feedbacks: {fb_count if fb_count is not None else 'n/a'}\n"
    )

    # Metrics block
    m = metrics_snapshot()
    top_lines = ", ".join([f"{cmd}:{cnt}" for cmd, cnt in m.get("top_commands", [])]) or "-"
    avg_lines = ", ".join([f"{cmd}:{avg}ms" for cmd, avg in m.get("avg_latency_ms", {}).items()]) or "-"
    text_msg += (
        "\nMetrics:\n"
        f"Total updates: {m.get('total_updates', 0)}\n"
        f"Top commands: {top_lines}\n"
        f"Avg latency: {avg_lines}\n"
    )
    await message.answer(text_msg)


def _calc_rss_mb() -> str:
    try:
        if resource is not None:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            rss_kb = usage.ru_maxrss
            # On Linux, ru_maxrss is in kilobytes; on macOS it can be bytes.
            if rss_kb > 0 and rss_kb < 1_000_000:  # assume KB
                return str(round(rss_kb / 1024, 1))
            return str(round(rss_kb / (1024*1024), 1))
    except Exception:
        pass
    # Fallback: unknown
    return "n/a"


def _load_avg() -> str:
    try:
        la = os.getloadavg()
        return f"{la[0]:.2f}/{la[1]:.2f}/{la[2]:.2f}"
    except Exception:
        return "n/a"
