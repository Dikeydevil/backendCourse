from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str = Field(description="title of hotel")
    name: str = Field(description="name of hotel")

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Новое значение title")
    name: str | None = Field(default=None, description="Новое значение name")
