import time
from typing import Optional

_started_at: Optional[float] = None


def mark_started() -> None:
    global _started_at
    _started_at = time.time()


def uptime_seconds() -> int:
    if _started_at is None:
        return 0
    return int(time.time() - _started_at)
