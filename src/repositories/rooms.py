from datetime import date
from typing import Any, Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomWithRels
from src.repositories.mappers.mappers import (
    RoomDataMapper,
    RoomDataWithRelsMapper,
)


class RoomsRepository(BaseRepository):
    model = RoomsOrm

    def __init__(
        self,
        session,
        *,
        mapper: Optional[RoomDataMapper] = None,
        mapper_with_rels: Optional[RoomDataWithRelsMapper] = None,
    ) -> None:
        super().__init__(session)
        self.mapper = mapper or RoomDataMapper()
        self.mapper_with_rels = mapper_with_rels or RoomDataWithRelsMapper()

    def _map_many_with_rels(self, models: Iterable[RoomsOrm]) -> list[RoomWithRels]:
        return [self.mapper_with_rels.map_to_domain_entity(m) for m in models]

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ) -> list[RoomWithRels]:
        room_ids = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.facilities))
            .where(RoomsOrm.id.in_(room_ids))
            .order_by(RoomsOrm.id)
        )
        res = await self.session.execute(query)
        orm_models = res.scalars().unique().all()
        return self._map_many_with_rels(orm_models)

    async def get_with_facilities(self, **filter_by: Any) -> Optional[RoomWithRels]:
        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.facilities))
            .filter_by(**filter_by)
        )
        res = await self.session.execute(query)
        orm_model = res.scalars().unique().one_or_none()
        return (
            None
            if orm_model is None
            else self.mapper_with_rels.map_to_domain_entity(orm_model)
        )

    async def get_one_with_facilities(self, **filter_by: Any) -> Optional[RoomWithRels]:
        return await self.get_with_facilities(**filter_by)
