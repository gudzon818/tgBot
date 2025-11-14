from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.main import main_menu
from bot.keyboards.inline import like_dislike_kb
from bot.i18n.translator import t
from bot.core.settings import settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message, lang: str) -> None:
    uid = message.from_user.id
    is_admin = False
    if settings.admin_ids:
        is_admin = uid in set(settings.admin_ids)
    elif settings.admin_id is not None:
        is_admin = uid == settings.admin_id
    await message.answer(t("start_greeting", lang), reply_markup=main_menu(lang, is_admin=is_admin))
    await message.answer(t("start_description", lang))
    await message.answer(t("rate_prompt", lang), reply_markup=like_dislike_kb(lang))
