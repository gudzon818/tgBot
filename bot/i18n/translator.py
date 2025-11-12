from typing import Dict

_DEFAULT_LOCALE = "ru"
_SUPPORTED = {"ru", "en"}

# Very simple per-process in-memory user language store
_user_langs: Dict[int, str] = {}

_texts: Dict[str, Dict[str, str]] = {
    "start_greeting": {
        "ru": "Привет! Бот запущен. 🚀",
        "en": "Hi! Bot started. 🚀",
    },
    "start_description": {
        "ru": (
            "Этот бот — мини‑игра, которая поможет тебе стать чуть лучше каждый день. "
            "Здесь ты найдёшь: задание на день, ответ 20‑гранного кубика, викторину и цитату дня."
        ),
        "en": (
            "This bot is a mini‑game to help you grow a bit every day. "
            "You’ll get: a daily task, a 20‑sided dice answer, a quiz, and a quote of the day."
        ),
    },
    "rate_prompt": {
        "ru": "Оцените бота: ChailyBot ",
        "en": "Rate the bot: ChailyBot",
    },
    "help": {
        "ru": (
            "Доступные команды:\n"
            "/start — старт и клавиатура\n"
            "/help — помощь\n"
            "/ping — проверить отклик бота\n"
            "/feedback — отправить отзыв\n"
            "/lang — сменить язык (ru/en)\n"
            "/daily — задание на день\n"
            "/d20 — 20‑гранный кубик\n"
            "/quiz — викторина\n"
            "/quote — цитата дня"
        ),
        "en": (
            "Available commands:\n"
            "/start — start and keyboard\n"
            "/help — help\n"
            "/ping — check latency\n"
            "/feedback — send feedback\n"
            "/lang — change language (ru/en)\n"
            "/daily — daily task\n"
            "/d20 — 20‑sided dice\n"
            "/quiz — quiz\n"
            "/quote — quote of the day"
        ),
    },
    "ping_pong": {"ru": "Pong! {ms} ms", "en": "Pong! {ms} ms"},
    "feedback_prompt": {
        "ru": "Напишите ваш отзыв одним сообщением.\nОтправьте /cancel чтобы отменить.",
        "en": "Send your feedback in a single message.\nUse /cancel to abort.",
    },
    "feedback_cancel_ok": {"ru": "Отменено.", "en": "Canceled."},
    "feedback_cancel_none": {"ru": "Нечего отменять.", "en": "Nothing to cancel."},
    "feedback_saved": {
        "ru": "Спасибо за отзыв! ✨ (сохранено)",
        "en": "Thanks for your feedback! ✨ (saved)",
    },
    "access_denied": {"ru": "Доступ запрещён.", "en": "Access denied."},
    "last_empty": {"ru": "Отзывов пока нет.", "en": "No feedback yet."},
    "last_header": {"ru": "Последние отзывы:", "en": "Latest feedback:"},
    "health_ok": {"ru": "ok", "en": "ok"},
    "like": {"ru": "👍 Нравится", "en": "👍 Like"},
    "dislike": {"ru": "👎 Не нравится", "en": "👎 Dislike"},
    "daily_title": {"ru": "Задание на сегодня:", "en": "Today’s task:"},
    "d20_title": {"ru": "Ответ кубика:", "en": "Dice says:"},
    "d20_cooldown": {"ru": "Подожди минуту перед следующим броском 🎲", "en": "Wait one minute before the next roll 🎲"},
    "d20_rolling": {"ru": "Бросаю кубик...", "en": "Rolling the die..."},
    "quiz_title": {"ru": "Викторина:", "en": "Quiz:"},
    "quiz_correct": {"ru": "Верно! ✅", "en": "Correct! ✅"},
    "quiz_wrong": {"ru": "Неверно. ❌", "en": "Wrong. ❌"},
    "quote_title": {"ru": "Цитата дня:", "en": "Quote of the day:"},
    "menu_daily": {"ru": "📅 Задание дня", "en": "📅 Daily task"},
    "menu_d20": {"ru": "🎲 Ответ кубика", "en": "🎲 20-sided dice"},
    "menu_quiz": {"ru": "❓ Викторина", "en": "❓ Quiz"},
    "menu_quote": {"ru": "✨ Цитата дня", "en": "✨ Quote of the day"},
    "daily_done_btn": {"ru": "✅ Выполнено", "en": "✅ Done"},
    "daily_skip_btn": {"ru": "🚫 Отказаться", "en": "🚫 Skip for today"},
    "daily_marked_done": {"ru": "Отлично! Задание отмечено выполненным.", "en": "Great! Task marked as done."},
    "daily_new": {"ru": "Вот ещё одно задание:", "en": "Here’s another task:"},
    "daily_category": {"ru": "Категория", "en": "Category"},
    "daily_difficulty": {"ru": "Сложность", "en": "Difficulty"},
    "difficulty_easy": {"ru": "лёгкая", "en": "easy"},
    "difficulty_medium": {"ru": "средняя", "en": "medium"},
    "difficulty_hard": {"ru": "сложная", "en": "hard"},
    "difficulty_gold": {"ru": "золото", "en": "gold"},
    "daily_awarded": {"ru": "Отлично! +{points} к рейтингу. Текущий рейтинг: {score}, стрик: {streak}.", "en": "Great! +{points} points. Score: {score}, streak: {streak}."},
    "daily_thanks": {"ru": "Отличная работа! 💪", "en": "Awesome job! 💪"},
    "daily_locked": {"ru": "Задание на сегодня уже получено. Новое будет доступно завтра.", "en": "You already had today’s task. A new one will be available tomorrow."},
    "daily_skip_locked": {"ru": "Хорошо. Новое задание будет доступно завтра.", "en": "Okay. A new task will be available tomorrow."},
    "me_title": {"ru": "Твой профиль:", "en": "Your profile:"},
    "me_line": {"ru": "Рейтинг: {score}\nСтрик: {streak}", "en": "Score: {score}\nStreak: {streak}"},
    "top_title": {"ru": "Топ 10:", "en": "Top 10:"},
    "top_empty": {"ru": "Пока пусто.", "en": "No data yet."},
}


def set_user_lang(user_id: int, lang: str) -> None:
    if lang in _SUPPORTED:
        _user_langs[user_id] = lang


def get_user_lang(user_id: int) -> str:
    return _user_langs.get(user_id, _DEFAULT_LOCALE)


def t(key: str, lang: str, **kwargs) -> str:
    variants = _texts.get(key)
    if not variants:
        return key
    text = variants.get(lang) or variants.get(_DEFAULT_LOCALE) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
