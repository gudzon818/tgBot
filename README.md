# Telegram Bot (aiogram)

## Local run
```bash
python bot/app.py
```

## День 14 — Alembic (миграции БД)

- В проект добавлена конфигурация Alembic:
  - `alembic.ini` — настройки.
  - `alembic/env.py` — async‑настройка, подключение `Base.metadata`, URL берётся из настроек.
  - `alembic/versions/` — папка для миграций.

### Генерация миграций

1) Убедитесь, что переменная окружения `DATABASE_URL` задана (как в `.env`).
2) Команды:
```bash
alembic revision -m "init" --autogenerate
alembic upgrade head
```

Подсказки:
- Если миграция пустая — проверьте, что все модели импортируются в `Base.metadata` (в проекте это уже сделано через `bot.infra.db` и импорт моделей внутри `init_db`).
- Для пересоздания миграции удалите файл из `alembic/versions` и перегенерируйте.

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

## День 3 — Логирование и Anti‑Flood

- Логирование включено на уровень `INFO` (формат: `%(asctime)s %(levelname)s %(name)s: %(message)s`).
- Добавлен `AntiFloodMiddleware` (ограничение частоты сообщений от одного пользователя, по умолчанию — 1 сообщение каждые 1.5 сек).

### Как проверить

1) Запуск (рекомендуемый способ из корня проекта):
```bash
python -m bot.app
```

2) В Telegram отправьте `/start` — бот ответит «Привет! Бот запущен. 🚀».

3) Отправьте несколько сообщений подряд быстро — часть из них будет проигнорирована антифлудом.

Советы:
- Чтобы видеть больше деталей, можно временно повысить уровень логирования до `DEBUG` в `bot/app.py`.

## День 5 — Inline‑кнопки и простой диалог (FSM)

- Добавлены Inline‑кнопки (лайк/дизлайк) и обработка `callback_data`.
- Добавлен простой диалог обратной связи `/feedback` на основе FSM (`MemoryStorage`).

### Команды и возможности

- `/start` — приветствие, Reply‑клавиатура и Inline‑оценка бота.
- `/help` — краткая справка по командам.
- `/ping` — проверка отклика бота.
- `/feedback` — бот попросит написать отзыв одним сообщением; `/cancel` — отмена диалога.

### Как проверить

1) Запуск:
```bash
python -m bot.app
```

2) Inline‑кнопки:
- В `/start` бот пришлёт: «Оцените бота: [👍 / 👎]».
- Нажмите кнопку — бот отправит ответ‑уведомление.

3) FSM (диалог отзыва):
- Отправьте `/feedback` — бот попросит текст отзыва.
- Отправьте сообщение с отзывом — бот ответит «Спасибо за отзыв! ✨» и завершит состояние.
- Если передумали — `/cancel`.

## День 6 — База данных (PostgreSQL) и отзывы

- Настройки окружения:
  - `DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tgbot`
  - `ADMIN_ID=<ваш_numeric_id>` (узнать: `/whoami`)

- Быстрый старт Postgres (Docker):
```bash
docker run --name tgbot-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=tgbot \
  -p 5432:5432 -d postgres:16
```

- Инициализация схемы:
  - Выполняется автоматически при старте бота (`init_db()`).

- Проверка отзывов:
  1) Запустите бота:
  ```bash
  python -m bot.app
  ```
  2) Отправьте `/feedback` и затем одно сообщение — бот ответит: «Спасибо за отзыв! ✨ (сохранено)»
  3) Отправьте `/last_feedbacks` — увидите до 10 последних отзывов (доступно только `ADMIN_ID`).

Подсказки:
- Если бот не видит БД — проверьте, запущен ли контейнер и корректен ли `DATABASE_URL`.
- После изменения `.env` перезапускайте бота.

## День 8 — Docker и docker-compose

- Файлы:
  - `Dockerfile` — образ бота (Python 3.12, requirements, entrypoint).
  - `.dockerignore` — исключения для контекста.
  - `docker-compose.yml` — сервисы: `db` (Postgres) и `bot`.
  - `entrypoint.sh` — ожидание БД, миграции Alembic, запуск бота.

### Запуск в контейнерах

1) Экспортируйте секреты окружения (или используйте .env в корне):
```bash
export BOT_TOKEN=...
export ADMIN_ID=...
export LOG_LEVEL=INFO
export LOG_FILE=/var/log/bot.log
```

2) Запуск:
```bash
docker compose up --build
```

3) Проверка:
- Бот стартует после готовности Postgres.
- Миграции применяются автоматически (`alembic upgrade head`).
- Команды и функционал работают как локально.

Остановка:
```bash
docker compose down
```

## День 10 — Redis: FSM и rate‑limit

- Настройки:
  - `REDIS_URL=redis://localhost:6379/0` (в контейнерах: `redis://redis:6379/0`)
- FSM‑хранилище:
  - При наличии Redis используется `RedisStorage`; иначе фолбэк `MemoryStorage`.
- Ограничение частоты (rate‑limit):
  - Через Redis (middleware), при отсутствии Redis — `AntiFloodMiddleware`.

### Как проверить
- Локально (без контейнеров):
  - Если Redis не установлен, всё работает с памятью. Для установки: `brew install redis && brew services start redis`.
  - Запуск бота: `python -m bot.app` — в логах при успехе Redis будет `FSM storage: RedisStorage`.
- В контейнерах: `docker compose up --build` — Redis поднимется автоматически.

## День 11 — Роли и inline‑пагинация

- Роли:
  - Фильтр `IsAdmin` (основан на `ADMIN_ID` из `.env`).
  - Команда `/admin` — доступ только админу.
- Inline‑пагинация:
  - Команда `/items` — демонстрационный список с кнопками Prev/Page/Next.

### Как проверить
- `/admin` — должно отвечать только вам (ADMIN_ID задан ранее).
- `/items` — листайте кнопками, обновляется сообщение и клавиатура.

## День 12 — Webhook (FastAPI)

- Переключатель режима:
  - `WEBHOOK_MODE=false` — polling (по умолчанию).
  - `WEBHOOK_MODE=true` — webhook‑режим (FastAPI, Uvicorn).
- Настройки вебхука:
  - `WEBHOOK_URL` — публичный HTTPS URL (например, https://your-domain.com).
  - `WEBHOOK_PATH` — путь для приёма обновлений (по умолчанию `/webhook`).
  - `WEB_HOST` и `WEB_PORT` — адрес и порт локального HTTP‑сервера.

### Локальная проверка (tunnel)

1) Получите внешний HTTPS URL:
   - ngrok: `ngrok http 8000` → возьмите `https://<subdomain>.ngrok.io`
   - либо Cloudflare Tunnel: `cloudflared tunnel --url http://localhost:8000`
2) В `.env` установите:
```
WEBHOOK_MODE=true
WEBHOOK_URL=<ваш_https_url>
WEBHOOK_PATH=/webhook
WEB_PORT=8000
```
3) Запуск:
```
python -m bot.app
```
4) Проверка:
   - GET http://localhost:8000/health → `{ "status": "ok" }`
   - В логах: `Webhook mode startup`
   - Telegram начнёт слать обновления на `<WEBHOOK_URL><WEBHOOK_PATH>`

### Прод

- Укажите реальный домен с HTTPS в `WEBHOOK_URL` и откройте порт `WEB_PORT` за reverse‑proxy (nginx/traefik/Caddy).
- В Docker:
  - Добавьте переменные `WEBHOOK_MODE=true`, `WEBHOOK_URL=...`, при необходимости пробросьте порт контейнера (например, `8000:8000`).
  - `docker compose up --build` — webhook будет активен автоматически.

Вернуться к polling: `WEBHOOK_MODE=false` и обычный запуск `python -m bot.app`.

## День 13 — CI/CD и /stats

- GitHub Actions:
  - Workflow: `.github/workflows/ci.yml` — ruff + pytest + docker build.
  - Триггеры: push в `main/master`, Pull Request.
  - Требования: `requirements.txt` в корне, при желании добавьте секреты для push образа.

- Ruff/pytest:
  - Конфиг: `pyproject.toml`.
  - Локальный запуск: `ruff check .` и `pytest`.

- /stats (для ADMIN_ID):
  - Команда выводит: uptime, статус Redis и DB, текущий LOG_LEVEL.
  - Пример: отправьте `/stats` в ЛС боту.

## День 15 — Автоматический Webhook и деплой

- При запуске в режиме webhook (`WEBHOOK_MODE=true`) бот автоматически вызывает `set_webhook`.
- Поддержан секрет `WEBHOOK_SECRET_TOKEN` — заголовок `X-Telegram-Bot-Api-Secret-Token` валидируется на входе.

### Быстрые шаги

1) В `.env` укажите:
```
WEBHOOK_MODE=true
WEBHOOK_URL=https://your-domain
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET_TOKEN=<случайная_строка>
```
2) Настройте reverse‑proxy (ниже примеры) и откройте 443/HTTPS.
3) Запустите контейнеры: `docker compose up -d`.
4) Проверьте `GET https://your-domain/health` → `{ "status": "ok" }`.

### Nginx (пример)

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain;

    ssl_certificate     /etc/letsencrypt/live/your-domain/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain/privkey.pem;

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        proxy_set_header Host $host;
        proxy_read_timeout 60s;
    }

    location /webhook {
        proxy_pass http://127.0.0.1:8000/webhook;
        proxy_set_header Host $host;
        proxy_read_timeout 60s;
    }
}
```

### Traefik (docker labels, пример)

```yaml
services:
  bot:
    image: ghcr.io/gudzon818/tgBot:latest
    environment:
      BOT_TOKEN: ${BOT_TOKEN}
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/tgbot
      REDIS_URL: redis://redis:6379/0
      WEBHOOK_MODE: "true"
      WEBHOOK_URL: https://your-domain
      WEBHOOK_PATH: /webhook
      WEBHOOK_SECRET_TOKEN: ${WEBHOOK_SECRET_TOKEN}
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.bot.rule=Host(`your-domain`) && PathPrefix(`/`)"
      - "traefik.http.routers.bot.entrypoints=websecure"
      - "traefik.http.routers.bot.tls=true"
      - "traefik.http.services.bot.loadbalancer.server.port=8000"
```

Замечания:
- Telegram сам добавляет заголовок `X-Telegram-Bot-Api-Secret-Token`; мы сверяем его с `WEBHOOK_SECRET_TOKEN`.
- Для polling‑режима просто установите `WEBHOOK_MODE=false`.

## День 16 — Персистентный i18n (язык в БД)

- Добавлена таблица `users` для хранения языка пользователя (`language_code`).
- Middleware `UserLocaleMiddleware` автоматически:
  - создаёт запись пользователя при первом обращении,
  - подставляет `lang` в handlers из БД (по умолчанию `ru`).
- Команда `/lang` теперь обновляет язык в БД.

### Миграция

```bash
alembic upgrade head
```

### Использование

- `/lang` — показать текущий язык и подсказку по команде.
- `/lang ru` или `/lang en` — сохранить язык в БД.

## День 18 — Тесты

- Конфигурация: `pyproject.toml` (pytest, ruff), директория `tests/`.
- Примеры тестов:
  - `test_translator.py` — переводы и форматирование.
  - `test_repos.py` — async‑тесты репозиториев на SQLite (in‑memory).
  - `test_middlewares.py` — метрики и latency.
  - `test_webhook.py` — интеграционный тест FastAPI webhook.

### Запуск

```bash
pytest -q
```

В CI прогоны выполняются автоматически (см. `.github/workflows/ci.yml`).

## День 19 — Роли и безопасность

- Мульти‑админы: `ADMIN_IDS` (список ID), fallback — `ADMIN_ID`.
- Фильтр `IsAdmin` поддерживает `Message`/`CallbackQuery` и проверяет список.
- Модерация:
  - `/mute <user_id> [seconds]` или reply + `/mute [seconds]` (по умолчанию 600s)
  - `/unmute <user_id>`
  - `/ban <user_id>`
  - `/unban <user_id>`
- Middleware:
  - `ModerationMiddleware` — блокировка banned и mute сообщений.
  - `CommandRateLimitMiddleware` — окна частоты на команды (`/ping` — 1s, `/feedback` — 10s).

### Настройка

В `.env`:
```
ADMIN_ID=<один_админ_необязательно>
ADMIN_IDS=123456,999999
```

## GHCR — публикация и использование Docker‑образа

- Пайплайн GitHub Actions публикует образ в GitHub Container Registry (GHCR):
  - Имя образа: `ghcr.io/<owner>/<repo>` (например, `ghcr.io/gudzon818/tgBot`).
  - При пуше в main публикуются теги: `latest` и `sha` (хэш коммита).
  - При пуше git‑тега в формате `vX.Y.Z` дополнительно публикуются: `X.Y.Z`, `X.Y`, `X`.

### Сделать пакет публичным

1) Откройте GitHub → ваш репозиторий → вкладка `Packages` → выберите пакет образа.
2) Нажмите `Manage package`.
3) В блоке Visibility выберите `Change visibility` → `Public` → подтвердите.

### Аутентификация и pull образа

- Если пакет публичный — логин не обязателен.
- Если приватный — авторизуйтесь:
  ```bash
  echo $GITHUB_TOKEN | docker login ghcr.io -u <your_github_username> --password-stdin
  ```

Скачать образ:
```bash
docker pull ghcr.io/gudzon818/tgBot:latest
```

### Запуск контейнера (polling)

```bash
docker run --rm \
  -e BOT_TOKEN=... \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db \
  -e REDIS_URL=redis://redis:6379/0 \
  -e WEBHOOK_MODE=false \
  -p 8000:8000 \
  ghcr.io/gudzon818/tgBot:latest
```

### Запуск контейнера (webhook)

```bash
docker run --rm \
  -e BOT_TOKEN=... \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db \
  -e REDIS_URL=redis://redis:6379/0 \
  -e WEBHOOK_MODE=true \
  -e WEBHOOK_URL=https://your-domain \
  -e WEBHOOK_PATH=/webhook \
  -e WEB_PORT=8000 \
  -p 8000:8000 \
  ghcr.io/gudzon818/tgBot:latest
```

### Пример docker-compose с образом из GHCR

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: tgbot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  bot:
    image: ghcr.io/gudzon818/tgBot:latest
    environment:
      BOT_TOKEN: ${BOT_TOKEN}
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/tgbot
      REDIS_URL: redis://redis:6379/0
      WEBHOOK_MODE: "false"
    depends_on:
      - db
      - redis
```
