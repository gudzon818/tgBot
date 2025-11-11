# bot/app.py
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.core.settings import settings
from bot.handlers.start import router as start_router
from bot.handlers.help import router as help_router
from bot.handlers.ping import router as ping_router
from bot.handlers.callbacks import router as callbacks_router
from bot.handlers.feedback import router as feedback_router
from bot.handlers.whoami import router as whoami_router
from bot.handlers.health import router as health_router
from bot.middlewares.anti_flood import AntiFloodMiddleware
from bot.infra.db import init_db, close_db


async def main() -> None:
    # Configure logging: console + rotating file based on settings
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    ch.setLevel(level)
    logger.addHandler(ch)
    fh = RotatingFileHandler(settings.log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    fh.setFormatter(fmt)
    fh.setLevel(level)
    logger.addHandler(fh)
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    # Middlewares
    dp.message.middleware.register(AntiFloodMiddleware(limit_seconds=1.5))
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(ping_router)
    dp.include_router(callbacks_router)
    dp.include_router(feedback_router)
    dp.include_router(whoami_router)
    dp.include_router(health_router)

    logging.info("Bot is starting long polling... (Day 7)")
    # Auto init DB schema
    try:
        await init_db()
        logging.info("Database initialized (or already up-to-date)")
    except Exception as e:
        logging.exception("Failed to init DB: %s", e)
    try:
        await dp.start_polling(bot)
    finally:
        await close_db()
        try:
            await bot.session.close()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())