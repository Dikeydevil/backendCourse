from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    password: str

class UserAdd(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    hashed_password: str

class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    firstname: str
    lastname: str
