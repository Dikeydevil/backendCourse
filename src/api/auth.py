from fastapi import APIRouter, HTTPException, Response

from src.api.dependecies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])



@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)
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
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Incorrect email or password"
            )
        AuthService().verify_password(data.password, user.hashed_password)
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token",access_token)
        return {"access_token": access_token}

@router.get("/me")
async def get_me(
        user_id: UserIdDep,
):

    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user