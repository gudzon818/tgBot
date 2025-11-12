import asyncio
import pytest
from aiogram.types import Message
from aiogram import F

from bot.middlewares.metrics import MetricsMiddleware
from bot.services.metrics import snapshot


@pytest.mark.asyncio
async def test_metrics_middleware_counts_latency(monkeypatch):
    mw = MetricsMiddleware()

    class DummyMessage:
        text = "/ping"
        from_user = type("U", (), {"id": 1, "username": "test"})()

    called = {"n": 0}

    async def handler(event, data):  # noqa: ARG001
        called["n"] += 1
        return True

    # run twice to accumulate
    await mw.__call__(handler, DummyMessage(), {})
    await mw.__call__(handler, DummyMessage(), {})

    m = snapshot()
    assert m["total_updates"] >= 2
    assert m["commands"].get("/ping", 0) >= 2
    assert m["avg_latency_ms"].get("/ping", 0) >= 0
