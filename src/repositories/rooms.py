from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        room_ids = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.facilities))
            .where(RoomsOrm.id.in_(room_ids))
            .order_by(RoomsOrm.id)
        )
        res = await self.session.execute(query)
        models = res.scalars().unique().all()
        return [RoomWithRels.model_validate(m, from_attributes=True) for m in models]

    async def get_with_facilities(self, **filter_by):
        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.facilities))
            .filter_by(**filter_by)
        )
        res = await self.session.execute(query)
        m = res.scalars().unique().one_or_none()
        return None if m is None else RoomWithRels.model_validate(m, from_attributes=True)

    async def get_one_with_facilities(self, **filter_by):
        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.facilities))
            .filter_by(**filter_by)
        )
        res = await self.session.execute(query)
        m = res.scalars().unique().one_or_none()
        return None if m is None else RoomWithRels.model_validate(m, from_attributes=True)
