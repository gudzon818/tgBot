from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.main import main_menu
from bot.keyboards.inline import like_dislike_kb
from bot.i18n.translator import t

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message, lang: str) -> None:
    await message.answer(t("start_greeting", lang), reply_markup=main_menu())
    await message.answer(t("rate_prompt", lang), reply_markup=like_dislike_kb(lang))
