"""
add_block_and_pin_code_to_users

Revision ID: 61bf3899b851
Revises: 1077519468df
Create Date: 2026-07-09 13:47:00.895717
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '61bf3899b851'
down_revision: str | None = '1077519468df'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("block", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("pin_code", sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "pin_code")
    op.drop_column("users", "block")
