from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class UserSessions(BaseModel):
    __tablename__ = "user_sessions"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    access_token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    access_token_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    refresh_token_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = ({"extend_existing": True},)
