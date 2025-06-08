from fastapi import FastAPI, Query, Body
from typing import Optional
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@app.get("/hotels")
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

@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })

@app.put("/hotels/{hotel_id}")
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

@app.patch("/hotels/{hotel_id}")
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


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
