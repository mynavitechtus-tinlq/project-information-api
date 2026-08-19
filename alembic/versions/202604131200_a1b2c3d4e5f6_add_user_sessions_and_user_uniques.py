"""add user_sessions and unique email/username on users

Revision ID: a1b2c3d4e5f6
Revises: 9f334eecb80b
Create Date: 2026-04-13 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "9f334eecb80b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_sessions",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("access_token", sa.String(length=500), nullable=False),
        sa.Column("refresh_token", sa.String(length=500), nullable=False),
        sa.Column("access_token_expires_at", sa.DateTime(), nullable=False),
        sa.Column("refresh_token_expires_at", sa.DateTime(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(), server_default="System", nullable=False),
        sa.Column("updated_by", sa.String(), server_default="System", nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk__user_sessions__user_id__users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user_sessions")),
        sa.UniqueConstraint("access_token", name=op.f("uq__user_sessions__access_token")),
        sa.UniqueConstraint("refresh_token", name=op.f("uq__user_sessions__refresh_token")),
    )
    op.create_index(
        op.f("ix__user_sessions_user_id"),
        "user_sessions",
        ["user_id"],
        unique=False,
    )
    op.create_unique_constraint(op.f("uq__users__email"), "users", ["email"])
    op.create_unique_constraint(op.f("uq__users__username"), "users", ["username"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq__users__username"), "users", type_="unique")
    op.drop_constraint(op.f("uq__users__email"), "users", type_="unique")
    op.drop_index(op.f("ix__user_sessions_user_id"), table_name="user_sessions")
    op.drop_table("user_sessions")
