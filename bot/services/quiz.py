from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class QuizItem:
    id: int
    question: str
    options: Sequence[str]
    correct_index: int


# Важно: порядок RU/EN синхронизирован, id = индекс + 1
_QUESTIONS_RU: list[tuple[str, list[str], int]] = [
    ("Столица Франции?", ["Берлин", "Париж", "Рим", "Мадрид"], 1),
    ("2 + 2 = ?", ["3", "4", "5", "22"], 1),
    ("Какой океан самый большой?", ["Атлантический", "Индийский", "Тихий", "Северный Ледовитый"], 2),
    ("Сколько континентов на Земле?", ["5", "6", "7", "8"], 2),
    ("Какой газ преобладает в атмосфере Земли?", ["Кислород", "Азот", "Углекислый газ", "Водород"], 1),
    ("Какой металл жидкий при комнатной температуре?", ["Железо", "Ртуть", "Алюминий", "Медь"], 1),
    ("Какую планету называют красной?", ["Венера", "Марс", "Юпитер", "Сатурн"], 1),
    ("Какое море самое солёное?", ["Чёрное", "Средиземное", "Мёртвое", "Балтийское"], 2),
    ("Кто написал 'Преступление и наказание'?", ["Толстой", "Достоевский", "Пушкин", "Чехов"], 1),
    ("Сколько градусов в прямом угле?", ["45", "90", "120", "180"], 1),
    # 10
    ("Какое животное самое крупное на Земле?", ["Слон", "Синий кит", "Жираф", "Бегемот"], 1),
    ("Какой орган перекачивает кровь?", ["Лёгкие", "Печень", "Сердце", "Почки"], 2),
    ("Как называется столица Японии?", ["Осака", "Киото", "Токио", "Нагоя"], 2),
    ("Сколько дней в високосном году?", ["364", "365", "366", "367"], 2),
    ("Какой цвет получается при смешении синего и жёлтого?", ["Зелёный", "Оранжевый", "Фиолетовый", "Красный"], 0),
    ("Как называется самая длинная река в мире?", ["Амазонка", "Нил", "Янцзы", "Волга"], 1),
    ("Какой инструмент измеряет температуру?", ["Барометр", "Термометр", "Амперметр", "Рулетка"], 1),
    ("Какой континент самый холодный?", ["Европа", "Азия", "Антарктида", "Северная Америка"], 2),
    ("Кто написал 'Евгений Онегин'?", ["Лермонтов", "Чехов", "Пушкин", "Гоголь"], 2),
    ("Сколько месяцев в году?", ["10", "11", "12", "13"], 2),
    # 20
    ("Какая планета ближе всего к Солнцу?", ["Меркурий", "Венера", "Земля", "Марс"], 0),
    ("Как зовут героя, который украл огонь у богов (греч. мифология)?", ["Геракл", "Прометей", "Персей", "Одиссей"], 1),
    ("Сколько часов в сутках?", ["12", "24", "36", "48"], 1),
    ("Как называется наука о растениях?", ["Зоология", "Ботаника", "Физика", "Астрономия"], 1),
    ("Какой орган отвечает за дыхание?", ["Печень", "Сердце", "Лёгкие", "Желудок"], 2),
    ("Какой океан омывает восточное побережье США?", ["Тихий", "Атлантический", "Индийский", "Северный Ледовитый"], 1),
    ("Как называется самая высокая гора в мире?", ["Килиманджаро", "Эверест", "Эльбрус", "Монблан"], 1),
    ("Какой прибор измеряет атмосферное давление?", ["Термометр", "Барометр", "Компас", "Спидометр"], 1),
    ("Сколько сторон у треугольника?", ["2", "3", "4", "5"], 1),
    ("Как называется крупнейший океан на Земле?", ["Индийский", "Атлантический", "Тихий", "Северный Ледовитый"], 2),
    # 30
    ("Кто является автором картины 'Мона Лиза'?", ["Микеланджело", "Леонардо да Винчи", "Рафаэль", "Рембрандт"], 1),
    ("Сколько минут в одном часе?", ["30", "45", "60", "90"], 2),
    ("Какая планета известна своими кольцами?", ["Марс", "Сатурн", "Юпитер", "Уран"], 1),
    ("Как называется процесс превращения воды в лёд?", ["Испарение", "Плавление", "Конденсация", "Замерзание"], 3),
    ("Столица Италии?", ["Милан", "Рим", "Неаполь", "Флоренция"], 1),
    ("Сколько дней в неделе?", ["5", "6", "7", "8"], 2),
    ("Какая страна самая большая по площади?", ["Канада", "Россия", "Китай", "США"], 1),
    ("Как называется прибор для измерения времени?", ["Часы", "Линейка", "Компас", "Барометр"], 0),
    ("Какой герой носил круглые очки и шрам в виде молнии?", ["Фродо", "Гарри Поттер", "Шерлок Холмс", "Бэтмен"], 1),
    ("Какая часть растения находится в земле?", ["Лист", "Стебель", "Корень", "Цветок"], 2),
    # 40
    ("Как называется наша галактика?", ["Туманность Андромеды", "Млечный Путь", "Большая Медведица", "Орион"], 1),
    ("Сколько секунд в одной минуте?", ["30", "40", "50", "60"], 3),
    ("Какой язык является государственным в Бразилии?", ["Испанский", "Португальский", "Английский", "Французский"], 1),
    ("Как называется учение о прошлом по вещественным источникам?", ["Геология", "Археология", "Социология", "Биология"], 1),
    ("Какой континент самый населённый?", ["Европа", "Азия", "Африка", "Южная Америка"], 1),
    ("Как называется самая маленькая единица вещества?", ["Молекула", "Атом", "Клетка", "Ион"], 1),
    ("Кто написал 'Война и мир'?", ["Толстой", "Достоевский", "Тургенев", "Гоголь"], 0),
    ("Какой цвет символизирует стоп на светофоре?", ["Зелёный", "Жёлтый", "Красный", "Синий"], 2),
    ("Сколько планет в Солнечной системе (сейчас)?", ["7", "8", "9", "10"], 1),
    ("Какой прибор показывает направление на север?", ["Барометр", "Компас", "Термометр", "Динамометр"], 1),
    # 50
    ("Как называется естественный спутник Земли?", ["Фобос", "Деймос", "Луна", "Ио"], 2),
    ("Какой орган отвечает за слух?", ["Глаз", "Ухо", "Язык", "Нос"], 1),
    ("Сколько сантиметров в одном метре?", ["10", "50", "100", "1000"], 2),
    ("Какой металл обозначается символом Fe?", ["Медь", "Железо", "Золото", "Серебро"], 1),
    ("Как называется учебное заведение после школы?", ["Детский сад", "Институт/университет", "Лицей", "Колледж"], 1),
    ("Какой праздник отмечают 1 января?", ["Рождество", "Новый год", "День труда", "День знаний"], 1),
    ("Как называется процесс, когда растения делают кислород из углекислого газа?", ["Фильтрация", "Фотосинтез", "Испарение", "Брожение"], 1),
    ("Столица Великобритании?", ["Лондон", "Манчестер", "Ливерпуль", "Эдинбург"], 0),
    ("Какой орган отвечает за зрение?", ["Ухо", "Нос", "Глаз", "Язык"], 2),
    ("Какой месяцу соответствует номер 12?", ["Октябрь", "Ноябрь", "Декабрь", "Январь"], 2),
    # 60
    ("Какой континент не имеет постоянного населения?", ["Антарктида", "Африка", "Австралия", "Европа"], 0),
    ("Как называется язык программирования для веб‑разметки?", ["Python", "HTML", "CSS", "SQL"], 1),
    ("Какой герой носит щит с изображением звезды?", ["Железный человек", "Капитан Америка", "Тор", "Халк"], 1),
    ("Сколько дней в феврале в невисокосный год?", ["28", "29", "30", "31"], 0),
    ("Как называется самая крупная пустыня мира?", ["Сахара", "Гоби", "Калахари", "Атакама"], 0),
    ("Какое животное символизирует Китайский Новый год по 12‑летнему циклу?", ["Слон", "Дракон", "Лошадь", "Крыса"], 3),
    ("Какой город называют 'городом любви'?", ["Рим", "Париж", "Вена", "Прага"], 1),
    ("Сколько ног у паука?", ["6", "8", "10", "12"], 1),
    ("Как называется прибор, измеряющий силу тока?", ["Вольтметр", "Амперметр", "Омметр", "Термометр"], 1),
    ("Как называется наука о звёздах и планетах?", ["География", "Астрономия", "Физика", "Химия"], 1),
    # 70
    ("Столица Германии?", ["Берлин", "Мюнхен", "Гамбург", "Кёльн"], 0),
    ("Как называется прибор для измерения массы?", ["Термометр", "Весы", "Барометр", "Компас"], 1),
    ("Какая планета известна как утренняя звезда?", ["Меркурий", "Венера", "Марс", "Юпитер"], 1),
    ("Сколько пальцев на одной руке у человека?", ["3", "4", "5", "6"], 2),
    ("Какой континент полностью находится в южном полушарии?", ["Австралия", "Европа", "Северная Америка", "Азия"], 0),
    ("Кто написал 'Маленький принц'?", ["Антуан де Сент‑Экзюпери", "Роальд Даль", "Льюис Кэрролл", "Жюль Верн"], 0),
    ("Какой инструмент с клавишами и педалями?", ["Скрипка", "Гитара", "Фортепиано", "Флейта"], 2),
    ("Сколько дней в апреле?", ["28", "29", "30", "31"], 2),
    ("Как называется основная единица измерения длины в СИ?", ["Сантиметр", "Метр", "Километр", "Миля"], 1),
    ("Какой праздник отмечают 8 марта?", ["День труда", "День знаний", "Международный женский день", "День Победы"], 2),
    # 80
    ("Как называется орган, который перекачивает кровь у человека?", ["Почка", "Сердце", "Печень", "Лёгкое"], 1),
    ("Какой океан находится между Европой и Америкой?", ["Тихий", "Атлантический", "Индийский", "Северный Ледовитый"], 1),
    ("Как называется столица Испании?", ["Барселона", "Мадрид", "Валенсия", "Севилья"], 1),
    ("Какой витамин получают из солнца?", ["Витамин A", "Витамин C", "Витамин D", "Витамин B"], 2),
    ("Сколько градусов в круге?", ["180", "270", "360", "90"], 2),
    ("Какой континент находится южнее всех?", ["Африка", "Австралия", "Южная Америка", "Антарктида"], 3),
    ("Как называется главный город страны?", ["Столица", "Область", "Деревня", "Посёлок"], 0),
    ("Как называется средство передвижения по рельсам?", ["Автобус", "Самолёт", "Поезд", "Корабль"], 2),
    ("Какой инструмент используют художники?", ["Отвёртка", "Кисть", "Штангенциркуль", "Молоток"], 1),
    ("Как называется большой водоём с солёной водой?", ["Озеро", "Река", "Море", "Пруд"], 2),
    # 90
    ("Как называется животное, которое живёт и в воде, и на суше?", ["Рыба", "Птица", "Амфибия", "Насекомое"], 2),
    ("Какой орган чувств помогает ощущать запахи?", ["Глаз", "Ухо", "Нос", "Язык"], 2),
    ("Какой металл обозначается символом Au?", ["Серебро", "Золото", "Алюминий", "Железо"], 1),
    ("Сколько часов в половине суток?", ["6", "10", "12", "24"], 2),
    ("Как называется единица измерения времени, равная 60 секундам?", ["Минута", "Час", "Сутки", "Неделя"], 0),
    ("Какой цвет получается при смешении красного и жёлтого?", ["Зелёный", "Оранжевый", "Фиолетовый", "Синий"], 1),
    ("Как называется наука о числах и фигурах?", ["Химия", "Физика", "Математика", "Биология"], 2),
    ("Какой орган позволяет слышать музыку?", ["Глаз", "Ухо", "Нос", "Кожа"], 1),
    ("Как называют изображение Земли на плоскости?", ["Глобус", "Карта", "Плакат", "Планшет"], 1),
    ("Как называется естественный спутник планеты?", ["Комета", "Астероид", "Луна", "Метеорит"], 2),
]


_QUESTIONS_EN: list[tuple[str, list[str], int]] = [
    ("Capital of France?", ["Berlin", "Paris", "Rome", "Madrid"], 1),
    ("2 + 2 = ?", ["3", "4", "5", "22"], 1),
    ("Which ocean is the largest?", ["Atlantic", "Indian", "Pacific", "Arctic"], 2),
    ("How many continents are on Earth?", ["5", "6", "7", "8"], 2),
    ("Which gas is most abundant in Earth's atmosphere?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], 1),
    ("Which metal is liquid at room temperature?", ["Iron", "Mercury", "Aluminum", "Copper"], 1),
    ("Which planet is called the Red Planet?", ["Venus", "Mars", "Jupiter", "Saturn"], 1),
    ("Which sea is the saltiest?", ["Black", "Mediterranean", "Dead", "Baltic"], 2),
    ("Who wrote 'Crime and Punishment'?", ["Tolstoy", "Dostoevsky", "Pushkin", "Chekhov"], 1),
    ("How many degrees are in a right angle?", ["45", "90", "120", "180"], 1),
    # 10
    ("What is the largest animal on Earth?", ["Elephant", "Blue whale", "Giraffe", "Hippo"], 1),
    ("Which organ pumps blood?", ["Lungs", "Liver", "Heart", "Kidneys"], 2),
    ("What is the capital of Japan?", ["Osaka", "Kyoto", "Tokyo", "Nagoya"], 2),
    ("How many days are in a leap year?", ["364", "365", "366", "367"], 2),
    ("What color do you get by mixing blue and yellow?", ["Green", "Orange", "Purple", "Red"], 0),
    ("Which is the longest river in the world?", ["Amazon", "Nile", "Yangtze", "Volga"], 1),
    ("Which instrument measures temperature?", ["Barometer", "Thermometer", "Ammeter", "Ruler"], 1),
    ("Which continent is the coldest?", ["Europe", "Asia", "Antarctica", "North America"], 2),
    ("Who wrote 'Eugene Onegin'?", ["Lermontov", "Chekhov", "Pushkin", "Gogol"], 2),
    ("How many months are in a year?", ["10", "11", "12", "13"], 2),
    # 20
    ("Which planet is closest to the Sun?", ["Mercury", "Venus", "Earth", "Mars"], 0),
    ("Who stole fire from the gods (Greek myth)?", ["Heracles", "Prometheus", "Perseus", "Odysseus"], 1),
    ("How many hours are in a day?", ["12", "24", "36", "48"], 1),
    ("What is the science of plants called?", ["Zoology", "Botany", "Physics", "Astronomy"], 1),
    ("Which organ is responsible for breathing?", ["Liver", "Heart", "Lungs", "Stomach"], 2),
    ("Which ocean borders the east coast of the USA?", ["Pacific", "Atlantic", "Indian", "Arctic"], 1),
    ("What is the highest mountain in the world?", ["Kilimanjaro", "Everest", "Elbrus", "Mont Blanc"], 1),
    ("Which device measures air pressure?", ["Thermometer", "Barometer", "Compass", "Speedometer"], 1),
    ("How many sides does a triangle have?", ["2", "3", "4", "5"], 1),
    ("Which is the largest ocean on Earth?", ["Indian", "Atlantic", "Pacific", "Arctic"], 2),
    # 30
    ("Who painted the Mona Lisa?", ["Michelangelo", "Leonardo da Vinci", "Raphael", "Rembrandt"], 1),
    ("How many minutes are in an hour?", ["30", "45", "60", "90"], 2),
    ("Which planet is famous for its rings?", ["Mars", "Saturn", "Jupiter", "Uranus"], 1),
    ("What is the process of water turning into ice called?", ["Evaporation", "Melting", "Condensation", "Freezing"], 3),
    ("Capital of Italy?", ["Milan", "Rome", "Naples", "Florence"], 1),
    ("How many days are in a week?", ["5", "6", "7", "8"], 2),
    ("Which country is the largest by area?", ["Canada", "Russia", "China", "USA"], 1),
    ("Which device measures time?", ["Clock", "Ruler", "Compass", "Barometer"], 0),
    ("Which hero wore round glasses and a lightning scar?", ["Frodo", "Harry Potter", "Sherlock Holmes", "Batman"], 1),
    ("Which part of a plant is in the ground?", ["Leaf", "Stem", "Root", "Flower"], 2),
    # 40
    ("What is the name of our galaxy?", ["Andromeda Nebula", "Milky Way", "Big Dipper", "Orion"], 1),
    ("How many seconds are in a minute?", ["30", "40", "50", "60"], 3),
    ("What is the official language of Brazil?", ["Spanish", "Portuguese", "English", "French"], 1),
    ("What science studies the past using artifacts?", ["Geology", "Archaeology", "Sociology", "Biology"], 1),
    ("Which continent has the largest population?", ["Europe", "Asia", "Africa", "South America"], 1),
    ("What is the smallest unit of matter?", ["Molecule", "Atom", "Cell", "Ion"], 1),
    ("Who wrote 'War and Peace'?", ["Tolstoy", "Dostoevsky", "Turgenev", "Gogol"], 0),
    ("Which color means 'stop' on a traffic light?", ["Green", "Yellow", "Red", "Blue"], 2),
    ("How many planets are in the Solar System now?", ["7", "8", "9", "10"], 1),
    ("Which device shows direction to the north?", ["Barometer", "Compass", "Thermometer", "Dynamometer"], 1),
    # 50
    ("What is Earth's natural satellite?", ["Phobos", "Deimos", "Moon", "Io"], 2),
    ("Which organ is responsible for hearing?", ["Eye", "Ear", "Tongue", "Nose"], 1),
    ("How many centimeters are in one meter?", ["10", "50", "100", "1000"], 2),
    ("Which metal has the symbol Fe?", ["Copper", "Iron", "Gold", "Silver"], 1),
    ("What is the educational institution after school?", ["Kindergarten", "University", "Lyceum", "College"], 1),
    ("Which holiday is celebrated on January 1?", ["Christmas", "New Year", "Labor Day", "Knowledge Day"], 1),
    ("What is the process when plants make oxygen from CO2?", ["Filtration", "Photosynthesis", "Evaporation", "Fermentation"], 1),
    ("Capital of the United Kingdom?", ["London", "Manchester", "Liverpool", "Edinburgh"], 0),
    ("Which organ is responsible for vision?", ["Ear", "Nose", "Eye", "Tongue"], 2),
    ("Which month is number 12?", ["October", "November", "December", "January"], 2),
    # 60
    ("Which continent has no permanent population?", ["Antarctica", "Africa", "Australia", "Europe"], 0),
    ("Which language is used for web markup?", ["Python", "HTML", "CSS", "SQL"], 1),
    ("Which hero carries a shield with a star?", ["Iron Man", "Captain America", "Thor", "Hulk"], 1),
    ("How many days are in February in a non‑leap year?", ["28", "29", "30", "31"], 0),
    ("What is the largest desert in the world?", ["Sahara", "Gobi", "Kalahari", "Atacama"], 0),
    ("Which animal symbolizes the start of the 12‑year Chinese cycle?", ["Elephant", "Dragon", "Horse", "Rat"], 3),
    ("Which city is called 'the city of love'?", ["Rome", "Paris", "Vienna", "Prague"], 1),
    ("How many legs does a spider have?", ["6", "8", "10", "12"], 1),
    ("Which device measures electric current?", ["Voltmeter", "Ammeter", "Ohmmeter", "Thermometer"], 1),
    ("What is the science of stars and planets called?", ["Geography", "Astronomy", "Physics", "Chemistry"], 1),
    # 70
    ("Capital of Germany?", ["Berlin", "Munich", "Hamburg", "Cologne"], 0),
    ("Which device measures mass?", ["Thermometer", "Scales", "Barometer", "Compass"], 1),
    ("Which planet is known as the morning star?", ["Mercury", "Venus", "Mars", "Jupiter"], 1),
    ("How many fingers on one human hand?", ["3", "4", "5", "6"], 2),
    ("Which continent lies entirely in the Southern Hemisphere?", ["Australia", "Europe", "North America", "Asia"], 0),
    ("Who wrote 'The Little Prince'?", ["Antoine de Saint‑Exupéry", "Roald Dahl", "Lewis Carroll", "Jules Verne"], 0),
    ("Which instrument has keys and pedals?", ["Violin", "Guitar", "Piano", "Flute"], 2),
    ("How many days are in April?", ["28", "29", "30", "31"], 2),
    ("What is the main SI unit of length?", ["Centimeter", "Meter", "Kilometer", "Mile"], 1),
    ("Which holiday is celebrated on March 8?", ["Labor Day", "Knowledge Day", "International Women's Day", "Victory Day"], 2),
    # 80
    ("Which organ pumps blood in the human body?", ["Kidney", "Heart", "Liver", "Lung"], 1),
    ("Which ocean is between Europe and America?", ["Pacific", "Atlantic", "Indian", "Arctic"], 1),
    ("What is the capital of Spain?", ["Barcelona", "Madrid", "Valencia", "Seville"], 1),
    ("Which vitamin do we get from sunlight?", ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin B"], 2),
    ("How many degrees are in a full circle?", ["180", "270", "360", "90"], 2),
    ("Which continent is farthest south?", ["Africa", "Australia", "South America", "Antarctica"], 3),
    ("What is the main city of a country called?", ["Capital", "Region", "Village", "Town"], 0),
    ("What vehicle moves on rails?", ["Bus", "Plane", "Train", "Ship"], 2),
    ("Which tool does a painter use?", ["Screwdriver", "Brush", "Caliper", "Hammer"], 1),
    ("What do we call a large body of salty water?", ["Lake", "River", "Sea", "Pond"], 2),
    # 90
    ("What animal lives both in water and on land?", ["Fish", "Bird", "Amphibian", "Insect"], 2),
    ("Which sense organ is used to smell?", ["Eye", "Ear", "Nose", "Tongue"], 2),
    ("Which metal has the symbol Au?", ["Silver", "Gold", "Aluminum", "Iron"], 1),
    ("How many hours are in half a day?", ["6", "10", "12", "24"], 2),
    ("What unit of time equals 60 seconds?", ["Minute", "Hour", "Day", "Week"], 0),
    ("What color do you get by mixing red and yellow?", ["Green", "Orange", "Purple", "Blue"], 1),
    ("What is the science of numbers and shapes?", ["Chemistry", "Physics", "Mathematics", "Biology"], 2),
    ("Which organ lets you hear music?", ["Eye", "Ear", "Nose", "Skin"], 1),
    ("What is the flat drawing of Earth called?", ["Globe", "Map", "Poster", "Tablet"], 1),
    ("What is a natural satellite of a planet called?", ["Comet", "Asteroid", "Moon", "Meteor"], 2),
]


def get_all(lang: str) -> Sequence[QuizItem]:
    bank = _QUESTIONS_RU if lang == "ru" else _QUESTIONS_EN
    return [
        QuizItem(id=i + 1, question=q, options=opts, correct_index=correct)
        for i, (q, opts, correct) in enumerate(bank)
    ]


def get_by_id(qid: int, lang: str) -> QuizItem:
    items = get_all(lang)
    if qid < 1 or qid > len(items):
        raise IndexError("quiz id out of range")
    return items[qid - 1]


def get_total() -> int:
    return len(_QUESTIONS_RU)


def pick_random_id(lang: str) -> int:
    # Просто для совместимости, если нужно случайное id
    return random.randint(1, get_total())
