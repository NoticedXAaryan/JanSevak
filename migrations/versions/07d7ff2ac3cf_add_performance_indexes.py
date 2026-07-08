"""
add_performance_indexes

Revision ID: 07d7ff2ac3cf
Revises: e3198948670c
Create Date: 2026-07-03 23:31:00.676225
"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "07d7ff2ac3cf"
down_revision: str | None = "e3198948670c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);")
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_conversations_user_active ON conversations(user_id) WHERE status = 'active';"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, created_at DESC);"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_reports_status ON anonymous_reports(status) WHERE status != 'resolved';"
    )
    # op.execute("CREATE INDEX IF NOT EXISTS idx_escalated_status ON escalated_queries(status) WHERE status = 'pending';")
    # Skipping escalated_queries since it might not exist yet, based on our models.


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_users_telegram_id;")
    op.execute("DROP INDEX IF EXISTS idx_conversations_user_active;")
    op.execute("DROP INDEX IF EXISTS idx_messages_conversation;")
    op.execute("DROP INDEX IF EXISTS idx_reports_status;")
    # op.execute("DROP INDEX IF EXISTS idx_escalated_status;")
