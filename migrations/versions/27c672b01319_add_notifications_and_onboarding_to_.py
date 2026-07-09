"""
add_notifications_and_onboarding_to_users

Revision ID: 27c672b01319
Revises: 61bf3899b851
Create Date: 2026-07-09 13:49:11.712847
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27c672b01319'
down_revision: Union[str, None] = '61bf3899b851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("notifications_enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False))
    op.add_column("users", sa.Column("onboarding_complete", sa.Boolean(), server_default=sa.text("false"), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "onboarding_complete")
    op.drop_column("users", "notifications_enabled")
