# bot/app.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.core.settings import settings
from bot.handlers.start import router as start_router


async def main() -> None:
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(start_router)

    print("Bot is starting long polling... (Day 2)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())