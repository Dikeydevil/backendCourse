from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException

from src.api.dependecies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date | None = Query(None, description="Дата заезда (включительно)"),
    date_to: date | None = Query(None, description="Дата выезда (исключительно)"),
):
    per_page = pagination.per_page or 5
    offset = per_page * (pagination.page - 1)
    if (date_from and not date_to) or (date_to and not date_from):
        raise HTTPException(status_code=400, detail="Укажите оба параметра: date_from и date_to")
    if date_from and date_to:
        return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=offset,
        )
    else:
        return await db.hotels.search_paginated(
            location=location,
            title=title,
            limit=per_page,
            offset=offset,
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.post("", summary="Создание нового отеля",
          description="Создание нового отеля")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples = {
    "1":{
        "summary": "Сочи",
        "value": {
            "title": "Plaza 5 звезд",
            "location": "Сочи пушкина "
                }
        },
    "2":{
        "summary": "Дубай",
        "value": {
            "title": "Allin",
            "location": "street 123"
                }
        }
    }
)
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}

@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="Частичное обновление данных об отеле, Частичное обнволение данных об отеле, Частичное обнволение данных об отеле")
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}