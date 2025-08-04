from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_filtered(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]
