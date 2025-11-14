import random
from datetime import date
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from bot.i18n.translator import t
from bot.services.daily_tasks import pick_random
from bot.infra.db import SessionLocal
from bot.repositories.daily_repo import DailyRepo, SCORES
from bot.services.d20 import pick_answer as d20_answer
from bot.services.cache import cache_get, cache_set
from bot.services.quiz import get_by_id as quiz_get_by_id, get_total as quiz_get_total, get_difficulty_by_id
from bot.repositories.quiz_repo import QuizRepo
from bot.services.quotes import get_by_id as quote_get_by_id, get_total as quote_get_total
from bot.repositories.quote_repo import QuoteRepo
from bot.services.horoscope import get_signs, get_random_horoscope
from bot.repositories.horoscope_repo import HoroscopeRepo
from bot.repositories.mood_repo import MoodRepo

router = Router()


@router.message(Command("daily"))
async def cmd_daily(message: types.Message, lang: str) -> None:
    # if user already interacted with today's task, lock
    async with SessionLocal() as session:
        repo = DailyRepo(session)
        if await repo.has_today(message.from_user.id):
            await message.answer(t("daily_locked", lang))
            return

    text, category_title, category_key, difficulty = pick_random(lang)
    diff_map = {
        "easy": t("difficulty_easy", lang),
        "medium": t("difficulty_medium", lang),
        "hard": t("difficulty_hard", lang),
        "gold": t("difficulty_gold", lang),
    }
    body = (
        f"{t('daily_title', lang)}\n"
        f"• {text}\n"
        f"{t('daily_category', lang)}: {category_title} | {t('daily_difficulty', lang)}: {diff_map.get(difficulty, difficulty)}"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("daily_done_btn", lang), callback_data=f"daily:done:{category_key}:{difficulty}"),
                InlineKeyboardButton(text=t("daily_skip_btn", lang), callback_data=f"daily:another:{category_key}:{difficulty}"),
            ]
        ]
    )
    await message.answer(body, reply_markup=kb)
    # log issued for today
    async with SessionLocal() as session:
        repo = DailyRepo(session)
        await repo.log_issued(message.from_user.id, category_key, difficulty)  # type: ignore[arg-type]


@router.message(Command("d20"))
async def cmd_d20(message: types.Message, lang: str) -> None:
    # Cooldown 60s per user
    key = f"d20:cd:{message.from_user.id}"
    if await cache_get(key):
        await message.answer(t("d20_cooldown", lang))
        return
    await cache_set(key, "1", ttl_seconds=60)
    # Rolling animation: send placeholder, then edit with result
    rolling = await message.answer(t("d20_rolling", lang) + " 🎲")
    try:
        await asyncio.sleep(1.5)
    except Exception:
        pass
    ans = d20_answer(lang)
    await rolling.edit_text(f"{t('d20_title', lang)} {ans}")


@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message, lang: str) -> None:
    async with SessionLocal() as session:
        repo = QuizRepo(session)
        total = quiz_get_total()
        qid = await repo.pick_next_question_id(message.from_user.id, total)
    if qid is None:
        await message.answer(t("quiz_completed", lang))
        return
    item = quiz_get_by_id(qid, lang)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=txt,
                    callback_data=f"quiz:{qid}:{i}",
                )
            ]
            for i, txt in enumerate(item.options)
        ]
    )
    await message.answer(f"{t('quiz_title', lang)} {item.question}", reply_markup=kb)


@router.callback_query(lambda c: c.data and c.data.startswith("quiz:"))
async def on_quiz_answer(call: types.CallbackQuery, lang: str) -> None:
    # data: quiz:<qid>:<chosen_index>
    try:
        _, qid_str, idx_str = (call.data or "").split(":", 2)
        qid = int(qid_str)
        chosen = int(idx_str)
    except Exception:
        await call.answer("OK")
        return

    item = quiz_get_by_id(qid, lang)
    is_correct = chosen == item.correct_index

    async with SessionLocal() as session:
        quiz_repo = QuizRepo(session)
        await quiz_repo.mark_answer(call.from_user.id, qid, is_correct)
        points = 0
        if is_correct:
            difficulty = get_difficulty_by_id(qid)
            # простое правило: easy=1, medium=2, hard=3
            quiz_scores = {"easy": 1, "medium": 2, "hard": 3}
            points = quiz_scores.get(difficulty, 1)
            daily_repo = DailyRepo(session)
            await daily_repo.award_quiz(call.from_user.id, call.from_user.username, points)

    if is_correct:
        await call.message.answer(t("quiz_correct", lang, points=points))
    else:
        await call.message.answer(t("quiz_wrong", lang))
    await call.answer()
    # После ответа сразу предложим следующий вопрос, если он есть
    if call.message is not None:
        await cmd_quiz(call.message, lang)


@router.message(Command("quote"))
async def cmd_quote(message: types.Message, lang: str) -> None:
    today = date.today()
    async with SessionLocal() as session:
        repo = QuoteRepo(session)
        # Если на сегодня уже выдавали цитату этому пользователю — больше не даём
        existing = await repo.get_today(message.from_user.id, today)
        if existing is not None:
            await message.answer(t("quote_locked_today", lang))
            return

        total = quote_get_total()
        qid = await repo.issue_new_for_today(message.from_user.id, today, total)
        if qid is None:
            await message.answer(t("quote_all_used", lang))
            return

    quote = quote_get_by_id(qid, lang)
    await message.answer(f"{t('quote_title', lang)}\n“{quote}”")


@router.message(Command("horoscope"))
async def cmd_horoscope(message: types.Message, lang: str) -> None:
    signs = get_signs(lang)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{s.emoji} {s.name_ru if lang == 'ru' else s.name_en}",
                    callback_data=f"hz:{s.code}",
                )
            ]
            for s in signs
        ]
    )
    header = "Выбери свой знак:" if lang == "ru" else "Choose your sign:"
    await message.answer(header, reply_markup=kb)


@router.message(Command("mood"))
async def cmd_mood(message: types.Message, lang: str) -> None:
    # 10 вариантов настроения с кодами
    options = [
        ("great", "😄"),
        ("good", "🙂"),
        ("ok", "😐"),
        ("tired", "😴"),
        ("stressed", "😵"),
        ("sad", "😔"),
        ("anxious", "😰"),
        ("angry", "😡"),
        ("bored", "🥱"),
        ("excited", "🤩"),
    ]
    # две строки по 5 кнопок
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for i, (code, emoji) in enumerate(options, start=1):
        label_key = f"mood_label_{code}"
        text = f"{emoji} {t(label_key, lang)}"
        row.append(InlineKeyboardButton(text=text, callback_data=f"md:{code}"))
        if i % 5 == 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    await message.answer(t("mood_prompt", lang), reply_markup=kb)


# Text button handlers (localized labels) that map to the same features
@router.message(F.text.in_([t("menu_daily", "ru"), t("menu_daily", "en")]))
async def on_menu_daily(message: types.Message, lang: str) -> None:
    await cmd_daily(message, lang)


@router.message(F.text.in_([t("menu_d20", "ru"), t("menu_d20", "en")]))
async def on_menu_d20(message: types.Message, lang: str) -> None:
    await cmd_d20(message, lang)


@router.message(F.text.in_([t("menu_quiz", "ru"), t("menu_quiz", "en")]))
async def on_menu_quiz(message: types.Message, lang: str) -> None:
    await cmd_quiz(message, lang)


@router.message(F.text.in_([t("menu_quote", "ru"), t("menu_quote", "en")]))
async def on_menu_quote(message: types.Message, lang: str) -> None:
    await cmd_quote(message, lang)


@router.message(F.text.in_([t("menu_horoscope", "ru"), t("menu_horoscope", "en")]))
async def on_menu_horoscope(message: types.Message, lang: str) -> None:
    await cmd_horoscope(message, lang)


@router.callback_query(lambda c: c.data and c.data.startswith("hz:"))
async def on_horoscope_select(call: types.CallbackQuery, lang: str) -> None:
    try:
        _, code = (call.data or "").split(":", 1)
    except Exception:
        await call.answer("OK")
        return

    today = date.today()
    async with SessionLocal() as session:
        repo = HoroscopeRepo(session)
        existing = await repo.get_today(call.from_user.id, today)
        if existing is not None:
            await call.answer("OK")
            await call.message.answer(t("horoscope_locked_today", lang))
            return
        # логируем выбранный знак на сегодня
        await repo.log_today(call.from_user.id, today, code)

    text = get_random_horoscope(code, lang)
    await call.message.answer(text)
    await call.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("md:"))
async def on_mood_select(call: types.CallbackQuery, lang: str) -> None:
    try:
        _, code = (call.data or "").split(":", 1)
    except Exception:
        await call.answer("OK")
        return
    today = date.today()
    async with SessionLocal() as session:
        repo = MoodRepo(session)
        await repo.log_today(call.from_user.id, today, code)
    await call.message.answer(t("mood_saved", lang))
    await call.answer("OK")


@router.callback_query(F.data.startswith("daily:done:"))
async def on_daily_done(call: types.CallbackQuery, lang: str) -> None:
    try:
        _, _, category_key, difficulty = (call.data or "").split(":", 3)
    except Exception:
        await call.answer("OK")
        await call.message.answer(t("daily_marked_done", lang))
        return
    # persist award
    async with SessionLocal() as session:
        repo = DailyRepo(session)
        score, streak = await repo.award_daily(
            user_id=call.from_user.id,
            username=call.from_user.username,
            category=category_key,
            difficulty=difficulty,  # type: ignore[arg-type]
        )
    points = SCORES.get(difficulty, 0)
    await call.answer("OK")
    await call.message.answer(t("daily_awarded", lang, points=points, score=score, streak=streak))
    await call.message.answer(t("daily_thanks", lang))


@router.callback_query(F.data.startswith("daily:another:"))
async def on_daily_another(call: types.CallbackQuery, lang: str) -> None:
    # log skip of previous suggested task (non-blocking try)
    try:
        _, _, category_key, difficulty_prev = (call.data or "").split(":", 3)
        async with SessionLocal() as session:
            repo = DailyRepo(session)
            await repo.log_skip(call.from_user.id, category_key, difficulty_prev)  # type: ignore[arg-type]
    except Exception:
        pass
    await call.answer("OK")
    # lock until tomorrow
    await call.message.answer(t("daily_skip_locked", lang))


@router.message(Command("me"))
async def cmd_me(message: types.Message, lang: str) -> None:
    async with SessionLocal() as session:
        daily_repo = DailyRepo(session)
        score, streak = await daily_repo.get_me(message.from_user.id)
        quiz_repo = QuizRepo(session)
        solved = await quiz_repo.get_solved_count(message.from_user.id)
    total = quiz_get_total()
    profile = t("me_line", lang, score=score, streak=streak)
    quiz_line = t("me_quiz", lang, solved=solved, total=total)
    progress = int(solved * 100 / total) if total else 0
    quiz_progress = t("me_quiz_progress", lang, progress=progress)
    await message.answer(f"{t('me_title', lang)}\n" + profile + "\n" + quiz_line + "\n" + quiz_progress)


@router.message(Command("top"))
async def cmd_top(message: types.Message, lang: str) -> None:
    async with SessionLocal() as session:
        repo = DailyRepo(session)
        rows = await repo.get_top(10)
    if not rows:
        await message.answer(t("top_empty", lang))
        return
    lines = []
    for i, (uid, uname, score) in enumerate(rows, start=1):
        name = uname or str(uid)
        lines.append(f"{i}. {name}: {score}")
    await message.answer(f"{t('top_title', lang)}\n" + "\n".join(lines))


@router.message(Command("mood_stats"))
async def cmd_mood_stats(message: types.Message, lang: str) -> None:
    async with SessionLocal() as session:
        repo = MoodRepo(session)
        stats = await repo.get_stats(message.from_user.id)
        days = await repo.get_total_days(message.from_user.id)

    if not stats:
        await message.answer(t("mood_advice_low_data", lang))
        return

    # формируем текст статистики
    lines: list[str] = [t("mood_stats_title", lang)]
    # упорядочим по коду для стабильности
    for code in [
        "great", "good", "ok", "tired", "stressed",
        "sad", "anxious", "angry", "bored", "excited",
    ]:
        cnt = stats.get(code)
        if not cnt:
            continue
        label_key = f"mood_label_{code}"
        label = t(label_key, lang)
        lines.append(t("mood_stats_line", lang, label=label, count=cnt))
    lines.append("")
    lines.append(t("mood_stats_days", lang, days=days))

    # простая оценка эмоционального фона
    positive = stats.get("great", 0) + stats.get("good", 0) + stats.get("excited", 0)
    neutral = stats.get("ok", 0) + stats.get("bored", 0)
    negative = (
        stats.get("tired", 0)
        + stats.get("stressed", 0)
        + stats.get("sad", 0)
        + stats.get("anxious", 0)
        + stats.get("angry", 0)
    )
    total = positive + neutral + negative
    if total < 3:
        advice = t("mood_advice_low_data", lang)
    else:
        if negative > positive and negative > neutral:
            advice = t("mood_advice_negative", lang)
        elif positive >= negative and positive >= neutral:
            advice = t("mood_advice_positive", lang)
        else:
            advice = t("mood_advice_mixed", lang)

    lines.append("")
    lines.append(advice)
    await message.answer("\n".join(lines))
