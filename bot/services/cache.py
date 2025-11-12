import time
from typing import Optional
import redis.asyncio as aioredis

from bot.core.settings import settings

# very simple hybrid cache: Redis if available, else in-memory with TTL
_memory_store: dict[str, tuple[float, str]] = {}
_redis: aioredis.Redis | None = None


async def _get_redis() -> aioredis.Redis | None:
    global _redis
    if _redis is not None:
        return _redis
    try:
        _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        await _redis.ping()
        return _redis
    except Exception:
        _redis = None
        return None


async def cache_get(key: str) -> Optional[str]:
    r = await _get_redis()
    if r:
        try:
            return await r.get(key)
        except Exception:
            pass
    # memory fallback
    item = _memory_store.get(key)
    if not item:
        return None
    expires_at, value = item
    if expires_at < time.monotonic():
        _memory_store.pop(key, None)
        return None
    return value


async def cache_set(key: str, value: str, ttl_seconds: int = 60) -> None:
    r = await _get_redis()
    if r:
        try:
            await r.setex(key, ttl_seconds, value)
            return
        except Exception:
            pass
    # memory fallback
    _memory_store[key] = (time.monotonic() + ttl_seconds, value)
