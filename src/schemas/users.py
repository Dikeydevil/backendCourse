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

    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    hashed_password: str
