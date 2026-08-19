from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_sessions_model import UserSessions
from app.repositories.base_repository import BaseRepository


class UserSessionRepository(BaseRepository[UserSessions, UUID]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_all_items(self) -> list[UserSessions]:
        results = await self.session.execute(select(UserSessions))
        return list(results.scalars().all())

    async def _get_item_by_id(self, item_id: UUID) -> UserSessions | None:
        results = await self.session.execute(select(UserSessions).where(UserSessions.id == item_id))
        return results.scalar_one_or_none()

    async def create_session(
        self,
        user_id: UUID,
        access_token: str,
        refresh_token: str,
        access_token_expires_at: datetime,
        refresh_token_expires_at: datetime,
    ) -> UserSessions:
        user_session = UserSessions(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_at=access_token_expires_at,
            refresh_token_expires_at=refresh_token_expires_at,
        )
        self.session.add(user_session)
        await self.session.commit()
        await self.session.refresh(user_session)
        return user_session

    async def get_by_access_token(self, access_token: str) -> UserSessions | None:
        results = await self.session.execute(select(UserSessions).where(UserSessions.access_token == access_token))
        return results.scalar_one_or_none()

    async def get_by_refresh_token(self, refresh_token: str) -> UserSessions | None:
        results = await self.session.execute(select(UserSessions).where(UserSessions.refresh_token == refresh_token))
        return results.scalar_one_or_none()

    async def delete_session_by_access_token(self, access_token: str) -> bool:
        result = await self.session.execute(delete(UserSessions).where(UserSessions.access_token == access_token))
        await self.session.commit()
        return result.rowcount > 0

    async def delete_all_for_user(self, user_id: UUID) -> int:
        result = await self.session.execute(delete(UserSessions).where(UserSessions.user_id == user_id))
        await self.session.commit()
        return result.rowcount
