from fastapi import Query, Body, APIRouter


router = APIRouter(prefix="/hotels")

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

@router.post("", summary="Создание нового отеля",
          description="<UNK> <UNK> <UNK> <UNK> <UNK> <UNK>")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })

@router.put("/{hotel_id}", summary="Обновление данных об отеле",
         description="<UNK> <UNK> <UNK> <UNK> <UNK> <UNK>")
def update_hotel_put(
    hotel_id: int,
    title: str = Body(..., description="Новое значение title"),
    name: str = Body(..., description="Новое значение name")
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "updated", "hotel": hotel}
    return {"status": "not found"}

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