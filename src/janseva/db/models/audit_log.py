"""AuditLog model — end-to-end tracking for all platform actions."""

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AuditLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    actor_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    actor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # "citizen", "dept_user", "system", "agent"

    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # login, query, report_submit, complaint_submit, status_change, policy_update, data_export

    resource_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    details_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    ip_address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
