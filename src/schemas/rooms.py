from pydantic import BaseModel, Field

class RoomAdd(BaseModel):
    hotel_id: int = Field(description="ID отеля")
    title: str = Field(description="Название комнаты")
    description: str | None = Field(default=None, description="Описание комнаты")
    price: float = Field(description="Цена за ночь")
    quantity: int = Field(description="Количество доступных номеров")

class Room(RoomAdd):
    id: int

class RoomPATCH(BaseModel):
    hotel_id: int | None = Field(default=None, description="ID отеля")
    title: str | None = Field(default=None, description="Название комнаты")
    description: str | None = Field(default=None, description="Описание комнаты")
    price: float | None = Field(default=None, description="Цена за ночь")
    quantity: int | None = Field(default=None, description="Количество доступных номеров")
