from aiogram import Router, types
from aiogram.filters import Command
from bot.i18n.translator import t

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message, lang: str) -> None:
    await message.answer(t("help", lang))
