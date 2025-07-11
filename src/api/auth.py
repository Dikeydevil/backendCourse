from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

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

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

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


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):

    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hased_password(email=data.email)
        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect email or password"
            )
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Incorrect email or password"
            )
        verify_password(data.password, user.hashed_password)
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token",access_token)
        return {"access_token": access_token}