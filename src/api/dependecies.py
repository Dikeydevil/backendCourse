from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    # по умолчанию page=1, обязательно int, минимум 1
    page: Annotated[int, Query(1, ge=1, description="Номер страницы")]
    # по умолчанию per_page=5, обязательно int, от 1 до 100
    per_page: Annotated[int, Query(5, ge=1, le=100, description="Элементов на страницу")]

PaginationDep = Annotated[PaginationParams, Depends()]
