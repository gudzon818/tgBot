from aiogram import Router, types
from aiogram.filters import Command
from bot.i18n.translator import t, get_user_lang

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    await message.answer(t("help", lang))
