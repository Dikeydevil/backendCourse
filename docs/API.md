# API справочник

Базовый URL: `http://127.0.0.1:8000`

Для эндпоинтов, помеченных как требующие аутентификации, необходима cookie `access_token` (выдаётся при `POST /auth/login`).

## Авторизация и аутентификация (`/auth`)

### POST /auth/register
Регистрация пользователя.

Тело запроса (JSON):
```json
{
  "email": "user@example.com",
  "username": "user01",
  "firstname": "Иван",
  "lastname": "Иванов",
  "password": "secret"
}
```
Ответ 200:
```json
{"status": "OK"}
```
Пример:
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user01","firstname":"Иван","lastname":"Иванов","password":"secret"}'
```

### POST /auth/login
Логин, устанавливает cookie `access_token` и возвращает токен.

Тело запроса как у регистрации (email + password используются для входа):
```json
{
  "email": "user@example.com",
  "username": "user01",
  "firstname": "Иван",
  "lastname": "Иванов",
  "password": "secret"
}
```
Ответ 200:
```json
{"access_token": "<JWT>"}
```
Пример с cookie:
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"user@example.com","username":"user01","firstname":"Иван","lastname":"Иванов","password":"secret"}'
```

### POST /auth/logout
Выход, удаляет cookie.
```bash
curl -X POST http://127.0.0.1:8000/auth/logout -b cookies.txt -c cookies.txt
```
Ответ 200:
```json
{"status":"success"}
```

### GET /auth/me
Текущий пользователь (требуется cookie).
```bash
curl http://127.0.0.1:8000/auth/me -b cookies.txt
```
Ответ 200 (пример):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user01",
  "firstname": "Иван",
  "lastname": "Иванов"
}
```

---

## Отели (`/hotels`)

### GET /hotels
Поиск и постраничная выдача.

Параметры query:
- `location` (str, опц.) — локация (частичное совпадение, регистронезависимо)
- `title` (str, опц.) — название отеля (частичное совпадение)
- `page` (int, по умолчанию 1, >=1)
- `per_page` (int, по умолчанию 5, 1..100)

Пример:
```bash
curl "http://127.0.0.1:8000/hotels?location=сочи&title=plaza&page=1&per_page=5"
```
Ответ 200:
```json
[
  {"id": 1, "title": "Plaza 5 звезд", "location": "Сочи пушкина"}
]
```

### GET /hotels/{hotel_id}
Получить один отель.
```bash
curl http://127.0.0.1:8000/hotels/1
```

### POST /hotels
Создать новый отель.

Тело запроса:
```json
{
  "title": "Plaza 5 звезд",
  "location": "Сочи пушкина"
}
```
Ответ 200:
```json
{"status": "OK", "data": {"id": 1, "title": "Plaza 5 звезд", "location": "Сочи пушкина"}}
```

### PUT /hotels/{hotel_id}
Полная замена данных об отеле.
```bash
curl -X PUT http://127.0.0.1:8000/hotels/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Plaza 6 звезд","location":"Сочи центр"}'
```
Ответ 200: `{ "status": "OK" }`

### PATCH /hotels/{hotel_id}
Частичное обновление данных.

Тело запроса (пример):
```json
{"location":"Сочи центр"}
```
Ответ 200: `{ "status": "OK" }`

### DELETE /hotels/{hotel_id}
Удалить отель.
```bash
curl -X DELETE http://127.0.0.1:8000/hotels/1
```
Ответ 200: `{ "status": "OK" }`

---

## Номера (`/hotels/{hotel_id}/rooms`)

### GET /hotels/{hotel_id}/rooms
Список номеров отеля.
```bash
curl http://127.0.0.1:8000/hotels/1/rooms
```

### GET /hotels/{hotel_id}/rooms/{room_id}
Получить номер.
```bash
curl http://127.0.0.1:8000/hotels/1/rooms/10
```

### POST /hotels/{hotel_id}/rooms
Создать номер.
```bash
curl -X POST http://127.0.0.1:8000/hotels/1/rooms \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Стандартный номер",
    "description":"Номер с одной кроватью",
    "price":4500,
    "quantity":5
  }'
```
Ответ 200: `{ "status": "OK", "data": {"id": 10, ...} }`

### PUT /hotels/{hotel_id}/rooms/{room_id}
Полная замена номера. Вернёт 404, если номер не найден.
```bash
curl -X PUT http://127.0.0.1:8000/hotels/1/rooms/10 \
  -H "Content-Type: application/json" \
  -d '{"title":"Обновлённый номер","description":"Две кровати","price":5200,"quantity":3}'
```
Ответ 200: `{ "status": "OK" }`

### PATCH /hotels/{hotel_id}/rooms/{room_id}
Частичное обновление номера.
```bash
curl -X PATCH http://127.0.0.1:8000/hotels/1/rooms/10 \
  -H "Content-Type: application/json" \
  -d '{"price":4990}'
```
Ответ 200: `{ "status": "OK" }`

### DELETE /hotels/{hotel_id}/rooms/{room_id}
Удалить номер.
```bash
curl -X DELETE http://127.0.0.1:8000/hotels/1/rooms/10
```
Ответ 200: `{ "status": "OK" }`

---

## Бронирования (`/bookings`)

### POST /bookings
Создать бронирование (требуется cookie).

Тело запроса:
```json
{
  "room_id": 10,
  "date_from": "2025-08-10",
  "date_to": "2025-08-15"
}
```
Пример:
```bash
curl -X POST http://127.0.0.1:8000/bookings \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"room_id":10,"date_from":"2025-08-10","date_to":"2025-08-15"}'
```
Ответ 200:
```json
{"status":"OK","data":{"id":1,"user_id":1,"room_id":10,"date_from":"2025-08-10","date_to":"2025-08-15","price":4500}}
```

### GET /bookings/
Список всех бронирований.
```bash
curl http://127.0.0.1:8000/bookings/
```
Ответ 200: `{ "status":"OK", "data": [ ... ] }`

### GET /bookings/me
Бронирования текущего пользователя (требуется cookie).
```bash
curl http://127.0.0.1:8000/bookings/me -b cookies.txt
```
Ответ 200: `{ "status":"OK", "data": [ ... ] }`

---

## Примечания
- Валидация и форматы данных описаны в `docs/SCHEMAS.md`.
- Пагинация для `/hotels` управляется query-параметрами `page` и `per_page`.
- Токен хранится в cookie `access_token`; срок жизни задаётся настройкой `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.