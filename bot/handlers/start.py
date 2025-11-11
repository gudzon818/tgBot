from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer("Привет! Бот запущен. 🚀")
