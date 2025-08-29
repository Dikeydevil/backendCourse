# Схемы данных

## Pydantic-схемы (`src/schemas/*`)

### Пользователи (`schemas/users.py`)
- `UserRequestAdd`
  - `email: EmailStr`
  - `username: str`
  - `firstname: str`
  - `lastname: str`
  - `password: str`
- `UserAdd`
  - `email: EmailStr`
  - `username: str`
  - `firstname: str`
  - `lastname: str`
  - `hashed_password: str`
- `User`
  - `id: int`
  - `email: EmailStr`
  - `username: str`
  - `firstname: str`
  - `lastname: str`
- `UserWithHashedPassword(User)`
  - `hashed_password: str`

### Отели (`schemas/hotels.py`)
- `HotelAdd`
  - `title: str` — название
  - `location: str` — локация
- `Hotel(HotelAdd)`
  - `id: int`
- `HotelPATCH`
  - `title: str | None`
  - `location: str | None`

### Номера (`schemas/rooms.py`)
- `RoomAddRequest`
  - `title: str`
  - `description: str | None`
  - `price: int`
  - `quantity: int`
- `RoomAdd`
  - `hotel_id: int`
  - `title: str`
  - `description: str | None`
  - `price: int`
  - `quantity: int`
- `Room(RoomAdd)`
  - `id: int`
- `RoomPatchRequest`
  - `title: str | None`
  - `description: str | None`
  - `price: int | None`
  - `quantity: int | None`
- `RoomPatch`
  - `hotel_id: int | None`
  - `title: str | None`
  - `description: str | None`
  - `price: int | None`
  - `quantity: int | None`

### Бронирования (`schemas/bookings.py`)
- `BookingAddRequest`
  - `room_id: int`
  - `date_from: date`
  - `date_to: date`
- `BookingAdd`
  - `user_id: int`
  - `room_id: int`
  - `date_from: date`
  - `date_to: date`
  - `price: int`
- `Booking(BookingAdd)`
  - `id: int`

---

## ORM-модели (`src/models/*`)

### UsersOrm
- `id: int (PK)`
- `email: str (unique)`
- `username: str (unique)`
- `firstname: str`
- `lastname: str`
- `hashed_password: str`

### HotelsOrm
- `id: int (PK)`
- `title: str`
- `location: str`

### RoomsOrm
- `id: int (PK)`
- `hotel_id: int (FK -> hotels.id)`
- `title: str`
- `description: str | None`
- `price: float`
- `quantity: int`

### BookingsOrm
- `id: int (PK)`
- `user_id: int (FK -> users.id)`
- `room_id: int (FK -> rooms.id)`
- `date_from: date`
- `date_to: date`
- `price: int`
- `total_cost: int` — гибридное свойство (`price * (date_to - date_from).days`)

---

## Общие замечания
- Все схемы ответа возвращаются в виде Pydantic-моделей, пригодных для сериализации в JSON.
- Для частичных обновлений используйте соответствующие `*Patch`-схемы и флаг `exclude_unset=True` при вызове репозиториев.
- Денежные значения представлены целыми числами или `float` (см. `RoomsOrm.price`). При необходимости нормализуйте типы под свою доменную логику.