from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.infra.db import SessionLocal
from bot.repositories.feedback_repo import FeedbackRepo
from bot.core.settings import settings
from bot.i18n.translator import t, get_user_lang

router = Router()


class FeedbackStates(StatesGroup):
    waiting_text = State()


@router.message(Command("feedback"))
async def cmd_feedback(message: types.Message, state: FSMContext) -> None:
    lang = get_user_lang(message.from_user.id)
    await state.set_state(FeedbackStates.waiting_text)
    await message.answer(t("feedback_prompt", lang))


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    lang = get_user_lang(message.from_user.id)
    if await state.get_state() is not None:
        await state.clear()
        await message.answer(t("feedback_cancel_ok", lang))
    else:
        await message.answer(t("feedback_cancel_none", lang))


@router.message(FeedbackStates.waiting_text)
async def feedback_receive(message: types.Message, state: FSMContext) -> None:
    lang = get_user_lang(message.from_user.id)
    text = message.text or "(empty)"
    async with SessionLocal() as session:
        repo = FeedbackRepo(session)
        await repo.add(user_id=message.from_user.id, text=text)
    await message.answer(t("feedback_saved", lang))
    await state.clear()


@router.message(Command("last_feedbacks"))
async def last_feedbacks(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    if settings.admin_id is None or message.from_user.id != settings.admin_id:
        await message.answer(t("access_denied", lang))
        return
    async with SessionLocal() as session:
        repo = FeedbackRepo(session)
        items = await repo.last(limit=10)
    if not items:
        await message.answer(t("last_empty", lang))
        return
    lines = [f"#{fb.id} • {fb.user_id}: {fb.text[:80]}" for fb in items]
    await message.answer(t("last_header", lang) + "\n" + "\n".join(lines))
