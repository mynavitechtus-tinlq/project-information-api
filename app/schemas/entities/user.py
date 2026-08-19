from uuid import UUID

from app.schemas.entities import BaseEntityModel


class UserModel(BaseEntityModel):
    id: UUID
    username: str
    email: str
    is_active: bool = True
