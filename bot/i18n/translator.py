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
            "📚 Помощь по боту\n\n"
            "🔹 Общие команды:\n"
            "  /start — старт и главное меню\n"
            "  /help — эта справка\n"
            "  /ping — проверить отклик бота\n"
            "  /feedback — отправить отзыв\n"
            "  /lang — сменить язык (ru/en)\n\n"
            "🎮 Игровой раздел:\n"
            "  Эти команды — мини‑игры и мотивация на каждый день.\n"
            "  /daily — задание дня (1 раз в сутки, даёт очки и стрик)\n"
            "  /d20 — 20‑гранный кубик с DnD‑ответами и минутным кулдауном\n"
            "  /quiz — викторина на 100 вопросов, прогресс и рейтинг сохраняются\n"
            "  /quote — цитата дня для вдохновения\n"
            "  /horoscope — гороскоп по знакам с лимитом один раз в день\n\n"
            "👤 Профиль, рейтинг и настроение:\n"
            "  /me — показать рейтинг, стрик и прогресс викторины\n"
            "  /top — топ‑10 по очкам\n"
            "  /mood — отметить сегодняшнее настроение (10 вариантов)\n"
            "  /mood_stats — посмотреть статистику настроения и общий совет"
        ),
        "en": (
            "📚 Bot help\n\n"
            "🔹 General commands:\n"
            "  /start — start and main menu\n"
            "  /help — this help\n"
            "  /ping — check latency\n"
            "  /feedback — send feedback\n"
            "  /lang — change language (ru/en)\n\n"
            "🎮 Game section:\n"
            "  These commands are mini‑games and daily motivation.\n"
            "  /daily — daily task (once per day, gives score and streak)\n"
            "  /d20 — 20‑sided dice with DnD‑style answers and 1‑minute cooldown\n"
            "  /quiz — quiz with 100 questions, progress and rating are saved\n"
            "  /quote — quote of the day for inspiration\n"
            "  /horoscope — horoscope by zodiac sign with one reading per day\n\n"
            "👤 Profile, rating and mood:\n"
            "  /me — show your score, streak and quiz progress\n"
            "  /top — top‑10 by score\n"
            "  /mood — log today’s mood (10 options)\n"
            "  /mood_stats — view mood stats and a general suggestion"
        ),
    },
    "help_admin": {
        "ru": (
            "🛡 Админские команды:\n"
            "  /stats — статистика бота (задержки, БД, Redis, модерация)\n"
            "  /mute <id> [сек] — временно заглушить пользователя\n"
            "  /unmute <id> — снять мут\n"
            "  /ban <id> — заблокировать пользователя\n"
            "  /unban <id> — снять бан"
        ),
        "en": (
            "🛡 Admin commands:\n"
            "  /stats — bot stats (latency, DB, Redis, moderation)\n"
            "  /mute <id> [seconds] — temporarily mute a user\n"
            "  /unmute <id> — unmute a user\n"
            "  /ban <id> — ban a user\n"
            "  /unban <id> — unban a user"
        ),
    },
    "menu_help": {"ru": "ℹ️ Помощь", "en": "ℹ️ Help"},
    "menu_admin_help": {"ru": "🛡 Админ меню", "en": "🛡 Admin menu"},
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
    "quiz_correct": {"ru": "Верно! ✅ +{points} к рейтингу.", "en": "Correct! ✅ +{points} points to your score."},
    "quiz_wrong": {"ru": "Неверно. ❌", "en": "Wrong. ❌"},
    "quiz_completed": {"ru": "Ты уже прошёл все вопросы викторины. 🎉", "en": "You have completed all quiz questions. 🎉"},
    "quote_title": {"ru": "Цитата дня:", "en": "Quote of the day:"},
    "quote_locked_today": {"ru": "Цитата на сегодня уже была. Приходи завтра за новой.", "en": "You already got today’s quote. Come back tomorrow for a new one."},
    "quote_all_used": {"ru": "Ты уже видел все доступные цитаты. 🎉", "en": "You have seen all available quotes. 🎉"},
    "menu_daily": {"ru": "📅 Задание дня", "en": "📅 Daily task"},
    "menu_d20": {"ru": "🎲 Ответ кубика", "en": "🎲 20-sided dice"},
    "menu_quiz": {"ru": "❓ Викторина", "en": "❓ Quiz"},
    "menu_quote": {"ru": "✨ Цитата дня", "en": "✨ Quote of the day"},
    "menu_horoscope": {"ru": "🔮 Гороскоп", "en": "🔮 Horoscope"},
    "menu_mood": {"ru": "🧠 Настроение", "en": "🧠 Mood"},
    "horoscope_locked_today": {"ru": "Гороскоп на сегодня уже был. Приходи завтра за новым.", "en": "You already got today’s horoscope. Come back tomorrow for a new one."},
    "mood_prompt": {"ru": "Какое у тебя сегодня настроение? Выбери один вариант:", "en": "How do you feel today? Pick one option:"},
    "mood_saved": {"ru": "Настроение сохранено. Спасибо за честность.", "en": "Mood saved. Thanks for being honest."},
    "mood_stats_title": {"ru": "Статистика настроения за всё время:", "en": "Mood stats for all time:"},
    "mood_stats_line": {"ru": "• {label}: {count}", "en": "• {label}: {count}"},
    "mood_stats_days": {"ru": "Всего дней с отметкой настроения: {days}", "en": "Total days with mood logged: {days}"},
    "mood_label_great": {"ru": "Отличное", "en": "Great"},
    "mood_label_good": {"ru": "Хорошее", "en": "Good"},
    "mood_label_ok": {"ru": "Нормальное", "en": "Okay"},
    "mood_label_tired": {"ru": "Усталость", "en": "Tired"},
    "mood_label_stressed": {"ru": "Стресс", "en": "Stressed"},
    "mood_label_sad": {"ru": "Грусть", "en": "Sad"},
    "mood_label_anxious": {"ru": "Тревога", "en": "Anxious"},
    "mood_label_angry": {"ru": "Злость", "en": "Angry"},
    "mood_label_bored": {"ru": "Скука", "en": "Bored"},
    "mood_label_excited": {"ru": "Воодушевление", "en": "Excited"},
    "mood_advice_low_data": {"ru": "Мало данных, чтобы делать выводы. Попробуй отмечать настроение хотя бы неделю подряд.", "en": "Too little data to say much. Try logging your mood for at least a week."},
    "mood_advice_positive": {"ru": "Похоже, у тебя преобладают позитивные дни. Сохраняй привычки, которые этому помогают.", "en": "Looks like you have mostly positive days. Keep the habits that support it."},
    "mood_advice_mixed": {"ru": "Настроение колеблется. Обрати внимание, какие дни идут лучше и что им помогает.", "en": "Your mood is mixed. Notice what makes the better days better and do more of that."},
    "mood_advice_negative": {"ru": "Негативных дней больше, чем хотелось бы. Постарайся добавить маленькие источники радости и поддержки, и при необходимости не стесняйся обратиться за помощью.", "en": "There are more negative days than you’d like. Try adding small sources of joy and support, and don’t hesitate to seek help if needed."},
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
    "me_line": {"ru": "Очки: {score}, стрик: {streak} дней", "en": "Score: {score}, streak: {streak} days"},
    "me_quiz": {"ru": "Викторина: {solved}/{total} правильных ответов", "en": "Quiz: {solved}/{total} correct answers"},
    "me_quiz_progress": {"ru": "Прогресс викторины: {progress}%", "en": "Quiz progress: {progress}%"},
    "top_title": {"ru": "🏆 Топ-10 по очкам", "en": "🏆 Top-10 by score"},
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
