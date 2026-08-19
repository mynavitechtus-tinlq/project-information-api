from uuid import UUID

from app.repositories.user_repository import UserRepository
from app.schemas.entities.user import UserModel


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all_users(self) -> list[UserModel]:
        users = await self.user_repository.get_all()

        return [UserModel.model_validate(user) for user in users]

    async def get_all_users_paginated(self, page: int, page_size: int) -> tuple[list[UserModel], int]:
        users, total_items = await self.user_repository.get_all_paginated(page=page, page_size=page_size)

        return [UserModel.model_validate(user) for user in users], total_items

    async def get_user(self, user_id: UUID) -> UserModel | None:
        user = await self.user_repository.get_item_by_id(user_id)

        return UserModel.model_validate(user) if user else None
