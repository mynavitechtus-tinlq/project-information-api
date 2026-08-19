from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    __table_args__ = ({"extend_existing": True},)
