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
import time

try:
    import resource  # type: ignore
except Exception:  # pragma: no cover
    resource = None  # type: ignore

from bot.services.metrics import snapshot as metrics_snapshot
from bot.services.moderation import stats as moderation_stats
router = Router()


@router.message(Command("admin"), IsAdmin())
async def cmd_admin(message: types.Message) -> None:
    await message.answer("Админ-панель: у вас есть доступ к административным командам.")


@router.message(Command("stats"), IsAdmin())
async def cmd_stats(message: types.Message) -> None:
    # Redis ping with latency
    redis_ok = False
    redis_latency_ms = None
    try:
        r = aioredis.from_url(settings.redis_url, decode_responses=True)
        t0 = time.perf_counter()
        pong = await r.ping()
        redis_latency_ms = int((time.perf_counter() - t0) * 1000)
        await r.close()
        redis_ok = bool(pong)
    except Exception:
        redis_ok = False

    # DB ping with latency
    db_ok = False
    fb_count = None
    db_latency_ms = None
    try:
        async with SessionLocal() as session:
            t1 = time.perf_counter()
            await session.execute(text("SELECT 1"))
            db_latency_ms = int((time.perf_counter() - t1) * 1000)
            db_ok = True
            res = await session.execute(select(func.count()).select_from(Feedback))
            fb_count = res.scalar() or 0
    except Exception:
        db_ok = False

    # Metrics
    m = metrics_snapshot()
    updates_total = int(m.get('total_updates', 0))
    up_s = max(uptime_seconds(), 1)
    updates_per_min = round(updates_total / (up_s / 60), 2)

    text_msg = (
        "Stats:\n"
        f"Uptime: {uptime_seconds()}s\n"
        f"Redis: {'OK' if redis_ok else 'FAIL'}"
        + (f" ({redis_latency_ms}ms)" if redis_latency_ms is not None else "") + "\n"
        f"DB: {'OK' if db_ok else 'FAIL'}"
        + (f" ({db_latency_ms}ms)" if db_latency_ms is not None else "") + "\n"
        f"Log level: {settings.log_level}\n"
        f"Mode: {'webhook' if settings.webhook_mode else 'polling'}\n"
        f"Version: {os.environ.get('APP_VERSION','dev')}\n"
        f"Git SHA: {os.environ.get('GIT_SHA','unknown')}\n"
        f"Aiogram: {getattr(aiogram, '__version__', 'unknown')}\n"
        f"RAM (RSS): {_calc_rss_mb()} MB\n"
        f"CPU load (1/5/15m): {_load_avg()}\n"
        f"Feedbacks: {fb_count if fb_count is not None else 'n/a'}\n"
        f"Updates: {updates_total} (≈{updates_per_min}/min)\n"
    )

    # Metrics block
    top_lines = ", ".join([f"{cmd}:{cnt}" for cmd, cnt in m.get("top_commands", [])]) or "-"
    avg_lines = ", ".join([f"{cmd}:{avg}ms" for cmd, avg in m.get("avg_latency_ms", {}).items()]) or "-"
    text_msg += (
        "\nMetrics:\n"
        f"Total updates: {m.get('total_updates', 0)}\n"
        f"Top commands: {top_lines}\n"
        f"Avg latency: {avg_lines}\n"
    )

    # Moderation block
    mod = moderation_stats()
    text_msg += (
        "\nModeration:\n"
        f"Backend: {mod.get('backend')}\n"
        f"Muted: {mod.get('muted_count')}\n"
        f"Banned: {mod.get('banned_count')}\n"
    )
    await message.answer(text_msg)


def _parse_target_args(message: types.Message) -> tuple[int | None, int | None]:
    """Return (user_id, seconds) from args or reply.
    Usage:
      /mute 123 60
      /mute 123
      reply to user's message with /mute 60
    """
    parts = (message.text or "").split()
    uid: int | None = None
    seconds: int | None = None
    # Try from args
    if len(parts) >= 2:
        try:
            uid = int(parts[1])
        except Exception:
            uid = None
    if len(parts) >= 3:
        try:
            seconds = int(parts[2])
        except Exception:
            seconds = None
    # If reply, prefer replied user id when not provided
    if uid is None and message.reply_to_message and message.reply_to_message.from_user:
        uid = message.reply_to_message.from_user.id
    return uid, seconds


@router.message(Command("mute"), IsAdmin())
async def cmd_mute(message: types.Message) -> None:
    uid, seconds = _parse_target_args(message)
    if uid is None:
        await message.answer("Usage: /mute <user_id> [seconds] (or reply to user)")
        return
    await mute(uid, seconds or 600)
    await message.answer(f"Muted {uid} for {seconds or 600}s")


@router.message(Command("unmute"), IsAdmin())
async def cmd_unmute(message: types.Message) -> None:
    uid, _ = _parse_target_args(message)
    if uid is None:
        await message.answer("Usage: /unmute <user_id> (or reply to user)")
        return
    await unmute(uid)
    await message.answer(f"Unmuted {uid}")


@router.message(Command("ban"), IsAdmin())
async def cmd_ban(message: types.Message) -> None:
    uid, _ = _parse_target_args(message)
    if uid is None:
        await message.answer("Usage: /ban <user_id> (or reply to user)")
        return
    await ban(uid)
    await message.answer(f"Banned {uid}")


@router.message(Command("unban"), IsAdmin())
async def cmd_unban(message: types.Message) -> None:
    uid, _ = _parse_target_args(message)
    if uid is None:
        await message.answer("Usage: /unban <user_id> (or reply to user)")
        return
    await unban(uid)
    await message.answer(f"Unbanned {uid}")


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
