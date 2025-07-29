from fastapi import APIRouter, Depends, HTTPException, status
from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingRequest, BookingAdd
from src.repositories.bookings import BookingsRepository
from src.repositories.rooms import RoomsRepository


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/")
async def create_booking(
    data: BookingRequest,
    db: DBDep,
    user_id: UserIdDep
):
    # Получаем цену комнаты из БД
    room_repo = RoomsRepository(db.session)
    room = await room_repo.get_one_or_none(id=data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    # Создаём новое бронирование
    booking_data = BookingAdd(
        room_id=data.room_id,
        user_id=user_id,  # Используем ID авторизованного пользователя
        date_from=data.date_from,
        date_to=data.date_to,
        price=room.price
    )

    booking_repo = BookingsRepository(db.session)
    new_booking = await booking_repo.add(booking_data)
    await db.commit()

    return {"status": "OK", "data": new_booking}
