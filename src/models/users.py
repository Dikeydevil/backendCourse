from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100),unique=True)
    username: Mapped[str] = mapped_column(String(100),unique=True)
    firstname: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(256))