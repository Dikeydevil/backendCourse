from fastapi import Query, Body, APIRouter
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@router.get("", summary="Получить данные об отелях",
         description="<UNK> <UNK> <UNK> <UNK>")
def get_hotels(
    id: Optional[int] = Query(default=None, description="Айдишник"),
    title: Optional[str] = Query(default=None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

class Hotel(BaseModel):
    title: str
    name: str

@router.post("", summary="Создание нового отеля",
          description="<UNK> <UNK> <UNK> <UNK> <UNK> <UNK>")
def create_hotel(hotel_data: Hotel,):
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
    title: Optional[str] = Body(default=None, description="Новое значение title"),
    name: Optional[str] = Body(default=None, description="Новое значение name")
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "patched", "hotel": hotel}
    return {"status": "not found"}


@router.delete("/{hotel_id}", summary="Удалить отель",)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}