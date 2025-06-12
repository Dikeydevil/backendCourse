from fastapi import Query, APIRouter, Body
from src.api.dependecies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
    {"id": 8, "title": "<UNK>", "name": "<UNK>"},
    {"id": 9, "title": "<UNK>", "name": "<UNK>"},
    {"id": 10, "title": "<UNK>", "name": "<UNK>"},
    {"id": 11, "title": "<UNK>", "name": "<UNK>"},
]

@router.get("", summary="Получить данные об отелях",
         description="<UNK> <UNK> <UNK> <UNK>")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, description="Айдишник"),
    title: str | None = Query(default=None, description="Название отеля"),

):
    hotels_ = []
    for hotel in hotels:
        if id is not None and hotel["id"] != id:
            continue
        if title is not None and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return hotels_



@router.post("", summary="Создание нового отеля",
          description="Создание нового отеля")
def create_hotel(hotel_data: Hotel = Body(openapi_examples = {
    "1":{
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд",
            "name": "ЛюКС Супер мега крутой отель"
                }
        }
    }
)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })

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