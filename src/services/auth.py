from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

from src.config import settings


class AuthService:
    pwd_context = CryptContext(
        schemes=["argon2"],
        default="argon2",
        deprecated="auto",
        argon2__time_cost=2,
        argon2__memory_cost=102400,
        argon2__parallelism=8,
    )

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")