from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import Users
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[Users, UUID]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_all_items(self) -> list[Users]:
        results = await self.session.execute(select(Users))

        return list(results.scalars().all())

    async def get_all_paginated(self, page: int, page_size: int) -> tuple[list[Users], int]:
        offset = (page - 1) * page_size

        results = await self.session.execute(select(Users).offset(offset).limit(page_size))
        total_results = await self.session.execute(select(func.count()).select_from(Users))

        return list(results.scalars().all()), int(total_results.scalar_one())

    async def _get_item_by_id(self, item_id: UUID) -> Users | None:
        results = await self.session.execute(select(Users).where(Users.id == item_id))

        return results.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Users | None:
        normalized_email = email.strip().lower()
        results = await self.session.execute(select(Users).where(func.lower(Users.email) == normalized_email))

        return results.scalar_one_or_none()
