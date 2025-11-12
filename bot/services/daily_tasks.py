import random
from dataclasses import dataclass
from typing import Literal, Sequence

Difficulty = Literal["easy", "medium", "hard", "gold"]


@dataclass(frozen=True)
class DailyTask:
    text_ru: str
    text_en: str
    category: str  # key
    difficulty: Difficulty


# 10 базовых категорий + 1 золотая
CATEGORIES: list[str] = [
    "health",
    "mindfulness",
    "learning",
    "fitness",
    "productivity",
    "social",
    "creativity",
    "organization",
    "finance",
    "digital_detox",
    "gold",
]

# Локализация названий категорий
CATEGORY_TITLES = {
    "health": {"ru": "Здоровье", "en": "Health"},
    "mindfulness": {"ru": "Осознанность", "en": "Mindfulness"},
    "learning": {"ru": "Обучение", "en": "Learning"},
    "fitness": {"ru": "Фитнес", "en": "Fitness"},
    "productivity": {"ru": "Продуктивность", "en": "Productivity"},
    "social": {"ru": "Социальное", "en": "Social"},
    "creativity": {"ru": "Креатив", "en": "Creativity"},
    "organization": {"ru": "Организация", "en": "Organization"},
    "finance": {"ru": "Финансы", "en": "Finance"},
    "digital_detox": {"ru": "Диджитал‑детокс", "en": "Digital detox"},
    "gold": {"ru": "Золотая задача", "en": "Gold challenge"},
}


TASKS: list[DailyTask] = [
    # Health (6)
    DailyTask("Выпей 2 стакана воды", "Drink two glasses of water", "health", "easy"),
    DailyTask("Сделай перекус из фрукта", "Have a fruit snack", "health", "easy"),
    DailyTask("Ляг спать на 30 минут раньше", "Go to bed 30 minutes earlier", "health", "medium"),
    DailyTask("Замени сладкое на орехи/йогурт", "Swap sweets for nuts/yogurt", "health", "medium"),
    DailyTask("Откажись от сладких напитков сегодня", "Skip sugary drinks today", "health", "hard"),
    DailyTask("Пройди 8 000 шагов", "Walk 8,000 steps", "health", "hard"),
    # Mindfulness (5)
    DailyTask("5 минут дыхательной практики", "5 minutes of breathing practice", "mindfulness", "easy"),
    DailyTask("Запиши 3 благодарности", "Write 3 things you're grateful for", "mindfulness", "easy"),
    DailyTask("10 минут медитации", "10 minutes meditation", "mindfulness", "medium"),
    DailyTask("Проведи 15 минут без телефона", "15 minutes without phone", "mindfulness", "medium"),
    DailyTask("Практикуй осознанную прогулку 20 минут", "Mindful walk for 20 minutes", "mindfulness", "hard"),
    # Learning (5)
    DailyTask("Прочитай 5 страниц книги", "Read 5 pages of a book", "learning", "easy"),
    DailyTask("Посмотри обучающее видео 10 минут", "Watch a 10-minute tutorial", "learning", "easy"),
    DailyTask("Законспектируй 3 факта", "Take notes on 3 facts", "learning", "medium"),
    DailyTask("Реши 5 задач по теме", "Solve 5 practice problems", "learning", "medium"),
    DailyTask("Напиши небольшой конспект (150 слов)", "Write a short 150-word summary", "learning", "hard"),
    # Fitness (5)
    DailyTask("Сделай 20 приседаний", "Do 20 squats", "fitness", "easy"),
    DailyTask("2 минуты планки", "2 minutes plank", "fitness", "medium"),
    DailyTask("3 подхода отжиманий", "3 sets of push-ups", "fitness", "medium"),
    DailyTask("Пробежка 2 км", "Run 2 km", "fitness", "hard"),
    DailyTask("Растяжка 10 минут", "Stretching for 10 minutes", "fitness", "easy"),
    # Productivity (5)
    DailyTask("Метод Pomodoro: 2 сессии", "Pomodoro: 2 sessions", "productivity", "medium"),
    DailyTask("Составь список дел на день", "Make a to-do list for today", "productivity", "easy"),
    DailyTask("Разбери 10 писем в почте", "Process 10 emails", "productivity", "easy"),
    DailyTask("Сделай одно "
              "сложное дело первым", "Do one hard task first", "productivity", "hard"),
    DailyTask("Отключи уведомления на 1 час", "Disable notifications for 1 hour", "productivity", "medium"),
    # Social (5)
    DailyTask("Напиши сообщение другу", "Text a friend", "social", "easy"),
    DailyTask("Позвони родным на 5 минут", "Call family for 5 minutes", "social", "easy"),
    DailyTask("Похвали коллегу/друга", "Give a compliment to a colleague/friend", "social", "medium"),
    DailyTask("Помоги кому‑то с задачей", "Help someone with a task", "social", "medium"),
    DailyTask("Встреться офлайн", "Meet offline", "social", "hard"),
    # Creativity (5)
    DailyTask("Сделай 1 набросок/фото", "Make one sketch/photo", "creativity", "easy"),
    DailyTask("Напиши 8 строк текста", "Write 8 lines of text", "creativity", "easy"),
    DailyTask("Найди 3 идеи для проекта", "Find 3 project ideas", "creativity", "medium"),
    DailyTask("30 минут творчества без отвлечений", "30 minutes of focused creativity", "creativity", "hard"),
    DailyTask("Сыграй мелодию/попробуй новый инструмент", "Play a melody/try a new instrument", "creativity", "medium"),
    # Organization (5)
    DailyTask("Убери один ящик/полку", "Tidy one drawer/shelf", "organization", "easy"),
    DailyTask("Разбери папку на рабочем столе", "Organize a desktop folder", "organization", "easy"),
    DailyTask("Ревизия задач на неделю", "Review your weekly tasks", "organization", "medium"),
    DailyTask("Наведи порядок в заметках", "Clean up your notes", "organization", "medium"),
    DailyTask("Оптимизируй рутину (1 шаг)", "Optimize a routine (1 step)", "organization", "hard"),
    # Finance (5)
    DailyTask("Запиши все траты за день", "Track all expenses today", "finance", "easy"),
    DailyTask("Откажись от импульсной покупки", "Skip an impulse buy", "finance", "medium"),
    DailyTask("Отложи 5% дохода", "Set aside 5% of income", "finance", "medium"),
    DailyTask("Проверь подписки и отмени лишнее", "Review and cancel unused subscriptions", "finance", "hard"),
    DailyTask("Прочитай статью про фин.грамотность", "Read an article on financial literacy", "finance", "easy"),
    # Digital detox (5)
    DailyTask("30 минут без соцсетей", "30 minutes without social media", "digital_detox", "easy"),
    DailyTask("Отключи лишние уведомления", "Turn off unnecessary notifications", "digital_detox", "medium"),
    DailyTask("Отложи телефон на 1 час", "Put your phone away for 1 hour", "digital_detox", "medium"),
    DailyTask("День без новостной ленты", "A day without news feed", "digital_detox", "hard"),
    DailyTask("Очисти домашний экран", "Clean up your home screen", "digital_detox", "easy"),
    # Gold (7)
    DailyTask("Тренировка 60 минут", "60-minute workout", "gold", "gold"),
    DailyTask("Сделай 10 000 шагов", "Walk 10,000 steps", "gold", "gold"),
    DailyTask("Глубокая работа 2 часа", "2 hours of deep work", "gold", "gold"),
    DailyTask("Напиши 1 000 слов", "Write 1,000 words", "gold", "gold"),
    DailyTask("Разбор финансов за месяц", "Monthly finance review", "gold", "gold"),
    DailyTask("Полное цифровое расхламление", "Full digital declutter", "gold", "gold"),
    DailyTask("Помоги незнакомцу значимо", "Meaningfully help a stranger", "gold", "gold"),
]


def _localize(text_ru: str, text_en: str, lang: str) -> str:
    return text_ru if lang == "ru" else text_en


def pick_random(lang: str) -> tuple[str, str, str, Difficulty]:
    """Return (task_text, category_title, category_key, difficulty)."""
    task = random.choice(TASKS)
    cat_title = CATEGORY_TITLES.get(task.category, {}).get(lang, task.category)
    return _localize(task.text_ru, task.text_en, lang), cat_title, task.category, task.difficulty
