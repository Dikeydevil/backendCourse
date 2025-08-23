from sqlalchemy import select, delete, insert
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility

class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def list_facility_ids(self, room_id: int) -> set[int]:
        res = await self.session.execute(
            select(self.model.facility_id).where(self.model.room_id == room_id)
        )
        return set(res.scalars().all())

    async def remove_extra(self, room_id: int, facility_ids: set[int]) -> None:
        if not facility_ids:
            return
        await self.session.execute(
            delete(self.model).where(
                self.model.room_id == room_id,
                self.model.facility_id.in_(facility_ids),
            )
        )

    async def add_missing(self, room_id: int, facility_ids: set[int]) -> None:
        if not facility_ids:
            return
        rows = [{"room_id": room_id, "facility_id": fid} for fid in facility_ids]
        await self.session.execute(insert(self.model).values(rows))

    async def replace_for_room(self, room_id: int, new_ids: set[int]) -> None:
        current_ids = await self.list_facility_ids(room_id)
        to_add = new_ids - current_ids
        to_remove = current_ids - new_ids
        await self.remove_extra(room_id, to_remove)
        await self.add_missing(room_id, to_add)
