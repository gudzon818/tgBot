from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ZodiacSign:
    code: str
    emoji: str
    name_ru: str
    name_en: str


_SIGNS: Sequence[ZodiacSign] = [
    ZodiacSign("aries", "♈", "Овен", "Aries"),
    ZodiacSign("taurus", "♉", "Телец", "Taurus"),
    ZodiacSign("gemini", "♊", "Близнецы", "Gemini"),
    ZodiacSign("cancer", "♋", "Рак", "Cancer"),
    ZodiacSign("leo", "♌", "Лев", "Leo"),
    ZodiacSign("virgo", "♍", "Дева", "Virgo"),
    ZodiacSign("libra", "♎", "Весы", "Libra"),
    ZodiacSign("scorpio", "♏", "Скорпион", "Scorpio"),
    ZodiacSign("sagittarius", "♐", "Стрелец", "Sagittarius"),
    ZodiacSign("capricorn", "♑", "Козерог", "Capricorn"),
    ZodiacSign("aquarius", "♒", "Водолей", "Aquarius"),
    ZodiacSign("pisces", "♓", "Рыбы", "Pisces"),
]


_HOROSCOPES_RU: dict[str, list[str]] = {
    "aries": [
        "Сегодня лучше сделать маленький шаг, чем большой план.",
        "Не бойся начать первым — но не забывай дослушивать других.",
        "Энергия есть — направь её в одно дело, а не в десять.",
        "Твоя честность сегодня — лучший фильтр людей.",
        "Не спорь с теми, кто не готов слушать. Сэкономишь силы.",
    ],
    "taurus": [
        "Стабильность сегодня важнее скорости.",
        "Небольшой комфорт сделает день продуктивнее.",
        "Хороший день, чтобы разложить по полкам дела и мысли.",
        "Не бойся сказать «нет» лишним обязанностям.",
        "Побалуй себя чем‑то вкусным — мозгу тоже нужен допинг.",
    ],
    "gemini": [
        "Сегодня слова особенно влияют — выбирай их внимательно.",
        "Идея придёт в движении, а не в переписке.",
        "Не держи всё в голове — запиши хотя бы три мысли.",
        "Хороший день, чтобы задать кому‑то честный вопрос.",
        "Если хочется всё успеть — выбери одно, но важное.",
    ],
    "cancer": [
        "Дом и уют сегодня заряжают сильнее, чем любой кофе.",
        "Позаботься о себе так, как заботишься о близких.",
        "Хороший день для небольшого эмоционального детокса.",
        "Не вини себя за усталость — она тоже часть пути.",
        "Тихий вечер может дать больше ответов, чем шумный день.",
    ],
    "leo": [
        "Сегодня мир чуть больше готов тебя услышать — используй это.",
        "Дай себе право гордиться маленькими победами.",
        "Не всё нужно делать ради впечатления. Сделай что‑то ради себя.",
        "Хороший день для смелого, но продуманного шага.",
        "Твоя уверенность заразительна — главное, чтобы она была честной.",
    ],
    "virgo": [
        "Сегодня список задач — твой лучший друг.",
        "Не пытайся исправить всё сразу — выбери одну область.",
        "Хороший день для небольшого улучшения привычного процесса.",
        "Твои стандарты высокие — не забудь добавить туда заботу о себе.",
        "Иногда «достаточно хорошо» — это именно то, что нужно.",
    ],
    "libra": [
        "Сегодня важен баланс: работа и отдых, люди и тишина.",
        "Если сомневаешься — задай ещё один уточняющий вопрос.",
        "Хороший момент, чтобы дипломатично закрыть старую тему.",
        "Согласие с собой важнее согласия со всеми.",
        "Небольшая прогулка поможет принять верное решение.",
    ],
    "scorpio": [
        "Интуиция сегодня особенно точна — но её стоит проверить фактами.",
        "Хороший день, чтобы тихо, но решительно что‑то изменить.",
        "Не трать энергию на борьбу там, где можно просто выйти из игры.",
        "Твоя глубина — сила, если не забывать всплывать.",
        "Иногда лучший ответ — не объяснять, а действовать.",
    ],
    "sagittarius": [
        "Сегодня день для расширения горизонтов — хоть немного.",
        "Новое знание может прийти из неожиданного источника.",
        "Планируй дальние цели, но начни с маленького шага сейчас.",
        "Хороший момент, чтобы вспомнить, ради чего ты вообще стараешься.",
        "Если хочется приключений — начни с маленького эксперимента.",
    ],
    "capricorn": [
        "Сегодня дисциплина вернёт вложенное с процентами.",
        "Сделай один важный шаг для будущего — даже если он незаметен.",
        "Хороший день для структурирования хаоса вокруг.",
        "Твоё терпение — ресурс, но его тоже нужно беречь.",
        "Иногда лучший прогресс — это держать курс, а не увеличивать скорость.",
    ],
    "aquarius": [
        "Сегодня нестандартная идея может решить стандартную проблему.",
        "Хороший момент, чтобы попробовать новый подход.",
        "Не бойся быть собой, даже если формат не предполагает.",
        "Твоя оригинальность — не баг, а фича.",
        "Если система не работает — подними вопрос, а не плечи.",
    ],
    "pisces": [
        "Сегодня важно прислушаться к себе, а не к шуму вокруг.",
        "Творчество в любой форме пойдёт на пользу.",
        "Хороший день для мягких, но честных разговоров.",
        "Сны и интуиция могут подсказать направление — но маршрут решаешь ты.",
        "Дай себе немного времени побыть в тишине.",
    ],
}

_HOROSCOPES_EN: dict[str, list[str]] = {
    "aries": [
        "Today a small step beats a big perfect plan.",
        "Don't be afraid to go first — just remember to listen.",
        "You have energy — aim it at one task, not ten.",
        "Your honesty is the best filter for people today.",
        "Don't argue with those who won't listen. Save your energy.",
    ],
    "taurus": [
        "Stability matters more than speed today.",
        "A bit of comfort will make you more productive.",
        "Good day to organize both tasks and thoughts.",
        "Don't be afraid to say no to extra obligations.",
        "Treat yourself to something tasty — your brain will thank you.",
    ],
    "gemini": [
        "Words have extra power today — choose them carefully.",
        "Ideas come in motion, not in chat threads.",
        "Don't keep everything in your head — write down at least three thoughts.",
        "Good day to ask someone an honest question.",
        "If you want to do everything, pick one important thing.",
    ],
    "cancer": [
        "Home and comfort recharge you more than coffee today.",
        "Take care of yourself the way you care for others.",
        "Good day for a small emotional detox.",
        "Don't blame yourself for being tired — it's part of the journey.",
        "A quiet evening may give more answers than a loud day.",
    ],
    "leo": [
        "The world is a bit more ready to hear you today — use it.",
        "Allow yourself to be proud of small wins.",
        "Not everything has to impress others. Do something just for you.",
        "Good day for a bold but well‑thought‑out move.",
        "Your confidence is contagious — make sure it's honest.",
    ],
    "virgo": [
        "A todo list is your best friend today.",
        "Don't try to fix everything at once — choose one area.",
        "Good day to slightly improve a routine process.",
        "Your standards are high — include self‑care in them too.",
        "Sometimes \"good enough\" is exactly what you need.",
    ],
    "libra": [
        "Balance is key today: work and rest, people and silence.",
        "If in doubt, ask one more clarifying question.",
        "Good moment to gracefully close an old topic.",
        "Being in agreement with yourself matters more than pleasing everyone.",
        "A short walk will help you decide.",
    ],
    "scorpio": [
        "Your intuition is sharp today — but still check the facts.",
        "Good day for quiet but decisive changes.",
        "Don't waste energy fighting where you can simply leave the game.",
        "Your depth is strength, as long as you remember to come up for air.",
        "Sometimes the best answer is action, not explanation.",
    ],
    "sagittarius": [
        "Today is a day for expanding horizons — even just a little.",
        "New knowledge may come from an unexpected source.",
        "Plan long‑term goals, but take a small step now.",
        "Good moment to remember why you're doing all this.",
        "If you crave adventure, start with a small experiment.",
    ],
    "capricorn": [
        "Discipline pays extra interest today.",
        "Take one small but important step for your future.",
        "Good day to bring structure to surrounding chaos.",
        "Your patience is a resource — don't waste it on nonsense.",
        "Sometimes progress is holding the course, not speeding up.",
    ],
    "aquarius": [
        "An unusual idea can solve a usual problem today.",
        "Good moment to try a new approach.",
        "Don't be afraid to be yourself, even if the format suggests otherwise.",
        "Your originality is not a bug, it's a feature.",
        "If a system doesn't work, raise the question, not your shoulders.",
    ],
    "pisces": [
        "Today listen to yourself more than to the noise around.",
        "Any form of creativity will do you good.",
        "Good day for gentle but honest conversations.",
        "Dreams and intuition can hint at direction — but you choose the route.",
        "Give yourself some time to be in silence.",
    ],
}


def get_signs(lang: str) -> Sequence[ZodiacSign]:
    return _SIGNS


def get_random_horoscope(sign_code: str, lang: str) -> str:
    pool = _HOROSCOPES_RU if lang == "ru" else _HOROSCOPES_EN
    items = pool.get(sign_code) or pool["aries"]
    return random.choice(items)
