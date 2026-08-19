import uuid
from datetime import datetime

from sqlalchemy import DateTime, MetaData, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

constraint_naming_conventions = {
    "ix": "ix__%(column_0_N_label)s",
    "uq": "uq__%(table_name)s__%(column_0_N_name)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(column_0_N_name)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=constraint_naming_conventions)


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(
        "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("uuid_generate_v4()")
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    created_by: Mapped[String] = mapped_column(String, default="System", server_default="System")
    updated_by: Mapped[String] = mapped_column(String, default="System", server_default="System")

    # @property
    # def id(self):
    #     return str(self._id)
