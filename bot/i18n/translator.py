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
    "rate_prompt": {
        "ru": "Оцените бота:",
        "en": "Rate the bot:",
    },
    "help": {
        "ru": (
            "Доступные команды:\n"
            "/start — старт и клавиатура\n"
            "/help — помощь\n"
            "/ping — проверить отклик бота\n"
            "/feedback — отправить отзыв\n"
            "/lang — сменить язык (ru/en)"
        ),
        "en": (
            "Available commands:\n"
            "/start — start and keyboard\n"
            "/help — help\n"
            "/ping — check latency\n"
            "/feedback — send feedback\n"
            "/lang — change language (ru/en)"
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
