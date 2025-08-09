# Внутренние компоненты

## Конфигурация (`src/config.py`)
Переменные окружения (см. `.env`):
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME` — параметры подключения к PostgreSQL
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` — параметры JWT

Сформированный URL подключения: `postgresql+asyncpg://<user>:<pass>@<host>:<port>/<db>`

## База данных (`src/database.py`)
- `engine = create_async_engine(settings.DB_URL)` — асинхронный движок
- `async_session_maker` — фабрика асинхронных сессий
- `Base` — декларативная база для ORM-моделей

## Менеджер БД (`src/utils/db_manager.py`)
Контекстный менеджер, предоставляющий доступ к репозиториям и управление транзакциями.

Использование:
```python
from src.database import async_session_maker
from src.utils.db_manager import DBManager

async with DBManager(session_factory=async_session_maker) as db:
    hotels = await db.hotels.get_all()
    await db.commit()
```
Свойства:
- `db.hotels`, `db.rooms`, `db.users`, `db.bookings` — экземпляры репозиториев
Методы:
- `commit()` — явный коммит транзакции

## Репозитории (слой доступа к данным)

### Базовый репозиторий (`src/repositories/base.py`)
Общие операции для всех сущностей.

Методы:
- `get_filtered(**filter_by)` → list[Schema] — выборка по фильтрам
- `get_all(*args, **kwargs)` → list[Schema] — эквивалент `get_filtered()` без фильтров
- `get_one_or_none(**filter_by)` → Schema | None — один объект или `None`
- `add(data: BaseModel)` → Schema — вставка и возврат созданной сущности
- `edit(data: BaseModel, exclude_unset: bool = False, **filter_by)` → None — обновление
- `delete(**filter_by)` → None — удаление

Примечания:
- Методы возвращают Pydantic-схемы, валидирующие ORM-объекты.
- Для частичных обновлений используйте `exclude_unset=True` и соответствующие схемы `*Patch`.

### Пользователи (`src/repositories/users.py`)
- `get_user_with_hased_password(email: EmailStr)` → `UserWithHashedPassword`
  - Возвращает пользователя с полем `hashed_password` по email.
  - Использует `one()`: при отсутствии записи поднимет исключение ORM. Обрабатывайте это на уровне сервиса/эндпоинта.

### Отели (`src/repositories/hotels.py`)
- Переопределён `get_all(location, title, limit, offset)`
  - Фильтрация по `location` и `title` (частичное совпадение, регистронезависимо)
  - Пагинация через `limit` и `offset`

### Номера (`src/repositories/rooms.py`)
- Наследует базовые операции без изменений

### Бронирования (`src/repositories/bookings.py`)
- Явное `get_filtered(**filter_by)` для выборки по пользователю и пр.

## Сервис аутентификации (`src/services/auth.py`)
Инкапсулирует хеширование паролей и работу с JWT.

- `hash_password(password: str) -> str` — Argon2-хеш
- `verify_password(plain: str, hashed: str) -> bool` — проверка пароля
- `create_access_token(data: dict) -> str` — создание JWT с `exp`
- `decode_token(token: str) -> dict` — декодирование JWT (бросает 401 при ошибке)

По умолчанию Argon2 настроен с повышенными параметрами безопасности (`time_cost=2`, `memory_cost=102400`, `parallelism=8`).

## Зависимости FastAPI (`src/api/dependecies.py`)
- `PaginationDep` — параметры пагинации (`page`, `per_page`)
- `UserIdDep` — извлекает `user_id` из cookie-токена
- `DBDep` — предоставляет `DBManager` через контекстный менеджер

Примечание: `get_token` читает cookie `access_token` и вызывает 401, если cookie отсутствует.