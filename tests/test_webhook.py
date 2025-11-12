from starlette.testclient import TestClient
from aiogram import Bot, Dispatcher

from bot.app import create_fastapi_app
from bot.core.settings import settings


def test_webhook_endpoint_ok(monkeypatch):
    # Prepare bot and dispatcher
    bot = Bot(token="123:ABC")

    called = {"n": 0, "payload": None}

    class DummyDP(Dispatcher):
        async def feed_update(self, _bot, update):  # type: ignore[override]
            called["n"] += 1
            called["payload"] = update

    dp = DummyDP()

    # Ensure no startup side-effects (no set_webhook)
    app = create_fastapi_app(bot, dp, redis_client=None, enable_startup=False)

    client = TestClient(app)

    # Build minimal Update
    payload = {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "date": 0,
            "chat": {"id": 1, "type": "private"},
            "from": {"id": 1, "is_bot": False, "first_name": "T"},
            "text": "/start",
        },
    }

    # If secret is set, provide header; else skip
    headers = {}
    if settings.webhook_secret_token:
        headers["X-Telegram-Bot-Api-Secret-Token"] = settings.webhook_secret_token

    r = client.post(settings.webhook_path, json=payload, headers=headers)
    assert r.status_code == 200
    assert r.json().get("ok") is True
    assert called["n"] == 1
    assert called["payload"] is not None
