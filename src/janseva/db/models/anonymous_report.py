"""
Anonymous report model.
CRITICAL: This table has NO foreign key to the users table.
The reporter's identity is never stored.
"""
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AnonymousReport(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "anonymous_reports"

    # Anonymous access token — reporter uses this to check status
    # This is the ONLY way to access the report. No user ID is stored.
    report_token: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )

    # Report classification
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    # Categories: corruption, misconduct, harassment, illegal_activity,
    #             public_safety, environmental, other

    # Encrypted content — never stored in plaintext
    content_encrypted: Mapped[str] = mapped_column(Text, nullable=False)

    # Where was this reported about?
    district: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Routing
    target_authority_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    routed_to_level: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    routed_to_department: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Organization link
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Relationships
    organization = relationship("Organization")

    # Status tracking
    status: Mapped[str] = mapped_column(
        String(20), default="submitted", nullable=False
    )
    # Statuses: submitted, under_review, investigating, resolved, dismissed

    # Admin-side notes (never shown to reporter directly to prevent info leakage)
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Severity assessment
    severity: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    # Severity: low, medium, high, critical
