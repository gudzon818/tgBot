# bot/app.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.core.settings import settings
from bot.handlers.start import router as start_router
from bot.handlers.help import router as help_router
from bot.handlers.ping import router as ping_router
from bot.middlewares.anti_flood import AntiFloodMiddleware


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # Middlewares
    dp.message.middleware.register(AntiFloodMiddleware(limit_seconds=1.5))
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(ping_router)

    logging.info("Bot is starting long polling... (Day 4)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())