from pydantic import BaseModel, Field, ConfigDict

class HotelAdd(BaseModel):
    title: str = Field(description="title of hotel")
    location: str = Field(description="name of hotel")

class Hotel(HotelAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Новое значение title")
    location: str | None = Field(default=None, description="Новое значение name")

    model_config = ConfigDict(from_attributes=True)
