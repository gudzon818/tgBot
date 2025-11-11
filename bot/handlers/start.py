from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.main import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer("Привет! Бот запущен. 🚀", reply_markup=main_menu())
