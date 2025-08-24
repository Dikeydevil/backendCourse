from pydantic import BaseModel, ConfigDict, Field

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

class RoomWithRels(Room):
    facilities: list[Facility]

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = Field(default=None, description="Название комнаты")
    description: str | None = Field(default=None, description="Описание комнаты")
    price: int | None = Field(default=None, description="Цена за ночь")
    quantity: int | None = Field(default=None, description="Количество доступных номеров")
    facilities_ids: list[int] | None = Field(
        default=None,
        description="Полный список удобств комнаты (заменяет текущие связи m2m)",
    )


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(default=None, description="ID отеля")
    title: str | None = Field(default=None, description="Название комнаты")
    description: str | None = Field(default=None, description="Описание комнаты")
    price: int | None = Field(default=None, description="Цена за ночь")
    quantity: int | None = Field(default=None, description="Количество доступных номеров")
