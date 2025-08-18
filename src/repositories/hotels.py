from datetime import date

from sqlalchemy import select, func, distinct

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def search_paginated(
        self,
        *,
        location: str | None,
        title: str | None,
        limit: int,
        offset: int,
    ) -> list[Hotel]:
        query = select(HotelsOrm)
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [Hotel.model_validate(h, from_attributes=True) for h in result.scalars().all()]

    async def get_filtered_by_time(
        self,
        *,
        date_from: date,
        date_to: date,
        location: str | None,
        title: str | None,
        limit: int,
        offset: int,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_subq = (
            select(distinct(RoomsOrm.hotel_id))
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_subq))
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [Hotel.model_validate(h, from_attributes=True) for h in result.scalars().all()]
