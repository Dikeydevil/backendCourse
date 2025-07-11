from pydantic import BaseModel, EmailStr, ConfigDict


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

class UserWithHashedPassword(User):
    model_config = ConfigDict(from_attributes=True)
    hashed_password: str
