# Telegram Bot (aiogram)

## Local run
```bash
python bot/app.py
```

## Подготовка окружения

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` из примера и вставьте токен бота:
```bash
cp .env.example .env
# отредактируйте .env и задайте BOT_TOKEN=<ваш_токен>
```

3. Запуск:
```bash
python bot/app.py
```

Бот поддерживает команду `/start`.
