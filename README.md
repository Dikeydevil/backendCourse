# Сервис бронирования отелей (FastAPI)

Современный backend-сервис на FastAPI для управления отелями, номерами и бронированиями, с авторизацией на JWT (через cookie) и асинхронной работой с БД (SQLAlchemy + asyncpg).

- Язык: Python 3.11+
- Фреймворк: FastAPI
- ORM: SQLAlchemy (async)
- БД: PostgreSQL
- Аутентификация: JWT (cookie `access_token`)

## Быстрый старт

1) Установите зависимости:

```bash
pip install -r requirements.txt
```

2) Подготовьте переменные окружения (файл `.env` рядом с `src/config.py`):

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=booking

JWT_SECRET_KEY=supersecret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

3) Запустите приложение:

```bash
cd src
python main.py
```

Приложение поднимется на `http://127.0.0.1:8000`. Автодокументация OpenAPI: `http://127.0.0.1:8000/docs`.

## Документация

- API (эндпоинты, примеры): `docs/API.md`
- Внутренние компоненты (сервисы, репозитории, базы данных): `docs/INTERNALS.md`
- Схемы данных (Pydantic и ORM-модели): `docs/SCHEMAS.md`

## Структура проекта (основное)

```
src/
  api/            # Маршруты FastAPI (auth, hotels, rooms, bookings)
  models/         # ORM-модели SQLAlchemy
  repositories/   # Репозитории (доступ к БД)
  schemas/        # Pydantic-схемы (запросы/ответы)
  services/       # Доменные сервисы (auth)
  utils/          # Утилиты (DBManager)
  database.py     # Подключение к БД, фабрика сессий
  config.py       # Настройки из .env
  main.py         # Точка входа FastAPI
```

## Аутентификация

- Регистрация: `POST /auth/register`
- Логин: `POST /auth/login` — устанавливает cookie `access_token`
- Текущий пользователь: `GET /auth/me` — требует cookie
- Выход: `POST /auth/logout` — удаляет cookie

Cookie автоматически используется браузером. В `curl` используйте ключи `-c` (сохранить) и `-b` (передать) cookie-файл.

## Лицензия

Код предоставляется «как есть». Используйте и модифицируйте под свои нужды.