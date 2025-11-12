# bot/app.py
import asyncio
import logging
from logging.handlers import RotatingFileHandler
import json
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, HTTPException
from aiogram.types import Update
import uvicorn

from bot.core.settings import settings
from bot.handlers.start import router as start_router
from bot.handlers.help import router as help_router
from bot.handlers.ping import router as ping_router
from bot.handlers.callbacks import router as callbacks_router
from bot.handlers.feedback import router as feedback_router
from bot.handlers.whoami import router as whoami_router
from bot.handlers.health import router as health_router
from bot.handlers.lang import router as lang_router
from bot.handlers.admin import router as admin_router
from bot.handlers.items import router as items_router
from bot.middlewares.anti_flood import AntiFloodMiddleware
from bot.middlewares.user_locale import UserLocaleMiddleware
from bot.middlewares.metrics import MetricsMiddleware
from bot.middlewares.rate_limit import RedisRateLimitMiddleware
from bot.middlewares.moderation import ModerationMiddleware
from bot.middlewares.cmd_rate_limit import CommandRateLimitMiddleware
from bot.middlewares.redis_cmd_rate_limit import RedisCommandRateLimitMiddleware
from bot.infra.db import init_db, close_db
from bot.services.runtime import mark_started


app: FastAPI | None = None


def create_fastapi_app(bot: Bot, dp: Dispatcher, redis_client: aioredis.Redis | None, enable_startup: bool = True) -> FastAPI:  # type: ignore[name-defined]
    web = FastAPI()

    if enable_startup:
        @web.on_event("startup")
        async def on_startup():
            if settings.webhook_url:
                await bot.set_webhook(
                    url=settings.webhook_url.rstrip("/") + settings.webhook_path,
                    secret_token=(settings.webhook_secret_token or None),
                )
            logging.info("Webhook mode startup")

        @web.on_event("shutdown")
        async def on_shutdown():
            try:
                await bot.delete_webhook(drop_pending_updates=True)
            except Exception:
                pass
            await close_db()
            try:
                await bot.session.close()
            except Exception:
                pass
            if redis_client is not None:
                try:
                    await redis_client.close()
                except Exception:
                    pass

    @web.get("/health")
    async def health():
        return {"status": "ok"}

    @web.post(settings.webhook_path)
    async def webhook(request: Request):
        if settings.webhook_secret_token:
            header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
            if header_token != settings.webhook_secret_token:
                raise HTTPException(status_code=403, detail="Forbidden")
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}

    return web


async def main() -> None:
    # Configure logging: console + rotating file based on settings
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(level)
    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
            obj = {
                "ts": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S"),
                "level": record.levelname,
                "logger": record.name,
                "msg": record.getMessage(),
            }
            return json.dumps(obj, ensure_ascii=False)

    json_fmt = JsonFormatter()
    ch = logging.StreamHandler()
    ch.setFormatter(json_fmt)
    ch.setLevel(level)
    logger.addHandler(ch)
    fh = RotatingFileHandler(settings.log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    fh.setLevel(level)
    logger.addHandler(fh)
    # Mark process start for uptime metrics
    mark_started()
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Try Redis FSM storage, fallback to memory if not available
    redis_client = None
    storage = None
    try:
        redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)
        # quick ping
        await redis_client.ping()
        storage = RedisStorage(redis=redis_client, key_builder=DefaultKeyBuilder(with_bot_id=True))
        logging.info("FSM storage: RedisStorage")
    except Exception as e:
        logging.warning("Redis unavailable, fallback to MemoryStorage: %s", e)
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    # Middlewares
    dp.message.middleware.register(UserLocaleMiddleware(default_lang="ru"))
    dp.callback_query.middleware.register(UserLocaleMiddleware(default_lang="ru"))
    dp.message.middleware.register(MetricsMiddleware())
    dp.callback_query.middleware.register(MetricsMiddleware())
    dp.message.middleware.register(ModerationMiddleware())
    dp.callback_query.middleware.register(ModerationMiddleware())
    # Per-command rate limits (drop if too frequent)
    if redis_client is not None:
        dp.message.middleware.register(
            RedisCommandRateLimitMiddleware(redis_client, windows={
                "/ping": 1,
                "/feedback": 10,
            }, default_window=0)
        )
    else:
        dp.message.middleware.register(
            CommandRateLimitMiddleware(windows={
                "/ping": 1.0,
                "/feedback": 10.0,
            }, default_window=0.0)
        )
    if redis_client is not None:
        dp.message.middleware.register(RedisRateLimitMiddleware(redis_client, window_seconds=1.5))
    else:
        dp.message.middleware.register(AntiFloodMiddleware(limit_seconds=1.5))
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(ping_router)
    dp.include_router(callbacks_router)
    dp.include_router(feedback_router)
    dp.include_router(whoami_router)
    dp.include_router(health_router)
    dp.include_router(lang_router)
    dp.include_router(admin_router)
    dp.include_router(items_router)

    logging.info("Bot is starting long polling... (Day 7)")
    # Auto init DB schema
    try:
        await init_db()
        logging.info("Database initialized (or already up-to-date)")
    except Exception as e:
        logging.exception("Failed to init DB: %s", e)
    if settings.webhook_mode:
        # Build FastAPI app for webhook mode
        global app
        app = create_fastapi_app(bot, dp, redis_client, enable_startup=True)
        # Run uvicorn server
        config = uvicorn.Config(app, host=settings.web_host, port=settings.web_port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
    else:
        try:
            await dp.start_polling(bot)
        finally:
            await close_db()
            try:
                await bot.session.close()
            except Exception:
                pass
            if redis_client is not None:
                try:
                    await redis_client.close()
                except Exception:
                    pass


if __name__ == "__main__":
    asyncio.run(main())