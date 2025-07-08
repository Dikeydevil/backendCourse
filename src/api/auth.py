from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(
    schemes=["argon2"],
    default="argon2",
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=102400,
    argon2__parallelism=8,
)

@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(
        email=data.email,
        username=data.username,
        firstname=data.firstname,
        lastname=data.lastname,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
