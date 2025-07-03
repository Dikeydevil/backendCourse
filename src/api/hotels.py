from fastapi import Query, APIRouter, Body


from src.api.dependecies import PaginationDep
from src.database import async_session_maker
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

@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="Частичное обновление данных об отеле, Частичное обнволение данных об отеле, Частичное обнволение данных об отеле")
async def partially_edit_hotel(
        hotel_id: int,
        otel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(otel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}