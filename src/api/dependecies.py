from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated [int | None, Query( None, ge=1, description="Номер страницы")]
    per_page: Annotated [int | None, Query( None, ge=1, le=100, lt=300, description="Количество элементов на страницу")]



PaginationDep = Annotated[PaginationParams, Depends()]