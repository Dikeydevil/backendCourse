from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.database import engine
from src.api.dependecies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить данные об отелях",
            description="Поиск отелей по названию и локации с частичным совпадением")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(default=None, description="Локация отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
):
    per_page=pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("", summary="Создание нового отеля",
          description="Создание нового отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples = {
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}

@router.put("/{hotel_id}", summary="Обновление данных об отеле",
         description="<UNK> <UNK> <UNK> <UNK> <UNK> <UNK>")
def update_hotel_put(
    hotel_id: int, hotel_data: Hotel,):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "updated", "hotel": hotel}


@router.patch("/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="Частичное обновление данных об отеле, Частичное обнволение данных об отеле, Частичное обнволение данных об отеле")
def update_hotel_patch(
    hotel_id: int,
        hotel_data: HotelPATCH,
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "patched", "hotel": hotel}
    return {"status": "not found"}


@router.delete("/{hotel_id}", summary="Удалить отель",)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}