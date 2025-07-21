from fastapi import APIRouter, Body
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPATCH

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("")
async def get_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()

@router.get("/{room_id}")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)

@router.post("")
async def create_room(room_data: RoomAdd = Body(
    openapi_examples={
        "Example 1": {
            "summary": "Single room",
            "value": {
                "hotel_id": 1,
                "title": "Single Room",
                "description": "Уютная одноместная комната",
                "price": 3500.0,
                "quantity": 5
            }
        },
        "Example 2": {
            "summary": "Double room",
            "value": {
                "hotel_id": 1,
                "title": "Double Room",
                "description": "Просторная комната с двумя кроватями",
                "price": 5500.0,
                "quantity": 3
            }
        }
    }
)):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{room_id}")
async def edit_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch("/{room_id}")
async def partially_edit_room(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.delete("/{room_id}")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}
