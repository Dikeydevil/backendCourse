from pydantic import BaseModel, ConfigDict, Field


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = Field(default=None, description="Название комнаты")
    description: str | None = Field(default=None, description="Описание комнаты")
    price: int | None = Field(default=None, description="Цена за ночь")
    quantity: int | None = Field(default=None, description="Количество доступных номеров")


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(default=None, description="ID отеля")
    title: str | None = Field(default=None, description="Название комнаты")
    description: str | None = Field(default=None, description="Описание комнаты")
    price: int | None = Field(default=None, description="Цена за ночь")
    quantity: int | None = Field(default=None, description="Количество доступных номеров")
