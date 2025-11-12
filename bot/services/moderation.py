import asyncio
from typing import Optional

import redis.asyncio as aioredis

from bot.core.settings import settings

# In-memory fallback stores
_muted: set[int] = set()
_banned: set[int] = set()

_redis_client: aioredis.Redis | None = None
_redis_lock = asyncio.Lock()


async def _get_redis() -> aioredis.Redis | None:
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    async with _redis_lock:
        if _redis_client is not None:
            return _redis_client
        try:
            _redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)
            await _redis_client.ping()
            return _redis_client
        except Exception:
            _redis_client = None
            return None


async def mute(user_id: int, seconds: Optional[int] = None) -> None:
    r = await _get_redis()
    if r:
        ttl = seconds or 600
        await r.setex(f"mute:{user_id}", ttl, "1")
    _muted.add(user_id)


async def unmute(user_id: int) -> None:
    r = await _get_redis()
    if r:
        await r.delete(f"mute:{user_id}")
    _muted.discard(user_id)


async def ban(user_id: int) -> None:
    r = await _get_redis()
    if r:
        await r.set(f"ban:{user_id}", "1")
    _banned.add(user_id)


async def unban(user_id: int) -> None:
    r = await _get_redis()
    if r:
        await r.delete(f"ban:{user_id}")
    _banned.discard(user_id)


async def is_muted(user_id: int) -> bool:
    r = await _get_redis()
    if r:
        try:
            v = await r.exists(f"mute:{user_id}")
            return bool(v)
        except Exception:
            pass
    return user_id in _muted


async def is_banned(user_id: int) -> bool:
    r = await _get_redis()
    if r:
        try:
            v = await r.exists(f"ban:{user_id}")
            return bool(v)
        except Exception:
            pass
    return user_id in _banned


def stats() -> dict:
    """Return moderation stats: backend and counts for in-memory sets.
    Note: when Redis is enabled, counts reflect only in-memory fallback (approximate).
    """
    backend = "redis" if _redis_client is not None else "memory"
    return {
        "backend": backend,
        "muted_count": len(_muted),
        "banned_count": len(_banned),
    }
