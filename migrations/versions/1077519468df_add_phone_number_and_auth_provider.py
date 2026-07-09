"""
add_phone_number_and_auth_provider

Revision ID: 1077519468df
Revises: 7977b9a8701c
Create Date: 2026-07-09 13:28:02.839129
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1077519468df'
down_revision: Union[str, None] = '7977b9a8701c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("auth_provider", sa.String(length=50), server_default="telegram", nullable=False))
    op.add_column("users", sa.Column("phone_number", sa.String(length=50), nullable=True))
    op.add_column("users", sa.Column("email", sa.String(length=255), nullable=True))
    op.create_index(op.f("ix_users_phone_number"), "users", ["phone_number"], unique=True)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_phone_number"), table_name="users")
    op.drop_column("users", "email")
    op.drop_column("users", "phone_number")
    op.drop_column("users", "auth_provider")
