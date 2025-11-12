import time
from collections import defaultdict
from typing import Dict, Tuple

# Simple in-memory metrics store
_total_updates: int = 0
_command_counts: Dict[str, int] = defaultdict(int)
_command_latency_sum_ms: Dict[str, float] = defaultdict(float)


def now_ms() -> float:
    return time.perf_counter() * 1000.0


def inc_update() -> None:
    global _total_updates
    _total_updates += 1


def inc_command(cmd: str) -> None:
    _command_counts[cmd] += 1


def add_latency(cmd: str, ms: float) -> None:
    _command_latency_sum_ms[cmd] += ms


def snapshot() -> Dict[str, object]:
    # Build average latency per command where available
    avgs: Dict[str, float] = {}
    for cmd, total in _command_counts.items():
        s = _command_latency_sum_ms.get(cmd, 0.0)
        avgs[cmd] = round(s / total, 1) if total > 0 else 0.0
    # Top commands by count
    top = sorted(_command_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return {
        "total_updates": _total_updates,
        "commands": dict(_command_counts),
        "avg_latency_ms": avgs,
        "top_commands": top,
    }
