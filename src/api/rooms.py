from datetime import date

from fastapi import APIRouter, Body, HTTPException, status, Query

from src.api.dependecies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_with_facilities(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body()
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude={"facilities_ids"}))
    room = await db.rooms.add(_room_data)

    fac_ids = set(room_data.facilities_ids or [])
    if fac_ids:
        await db.rooms_facilities.add_missing(room.id, fac_ids)

    await db.commit()
    return {"status": "OK", "data": room}



@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest = Body(...)
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude={"facilities_ids"}))
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    await db.rooms.edit(_room_data, id=room_id)

    if room_data.facilities_ids is not None:
        await db.rooms_facilities.replace_for_room(room_id, set(room_data.facilities_ids))

    await db.commit()
    return {"status": "OK"}



@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest = Body(...)
):
    _room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude_unset=True, exclude={"facilities_ids"})
    )
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)

    if room_data.facilities_ids is not None:
        await db.rooms_facilities.replace_for_room(room_id, set(room_data.facilities_ids))

    await db.commit()
    return {"status": "OK"}



@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}