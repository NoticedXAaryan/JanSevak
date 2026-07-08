"""add variety and grade to mandi_prices

Revision ID: 7977b9a8701c
Revises: 3fa1e3112e01
Create Date: 2026-07-04
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7977b9a8701c"
down_revision = "3fa1e3112e01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("mandi_prices", sa.Column("variety", sa.String(255), nullable=True))
    op.add_column("mandi_prices", sa.Column("grade", sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column("mandi_prices", "grade")
    op.drop_column("mandi_prices", "variety")
