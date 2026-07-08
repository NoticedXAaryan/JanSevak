"""
Anonymous report model.
CRITICAL: This table has NO foreign key to the users table.
The reporter's identity is never stored.
"""

import uuid

import sqlalchemy
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AnonymousReport(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "anonymous_reports"

    # Anonymous access token — reporter uses this to check status
    # This is the ONLY way to access the report. No user ID is stored.
    report_token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)

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

    # Department link
    department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Sealed Envelope Identity (Accountability Mechanism)
    # Encrypted with a dual-key system. Cannot be decrypted by a single admin.
    identity_envelope_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_flagged_fake: Mapped[bool] = mapped_column(default=False, nullable=False)
    fake_flag_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    decryption_authorized_by: Mapped[list[str] | None] = mapped_column(
        sqlalchemy.JSON, nullable=True
    )

    # Evidence
    evidence_image_urls: Mapped[list[str] | None] = mapped_column(
        sqlalchemy.ARRAY(String), nullable=True
    )

    # Relationships
    department = relationship("Department")

    # Status tracking
    status: Mapped[str] = mapped_column(String(20), default="submitted", nullable=False)
    # Statuses: submitted, under_review, investigating, resolved, dismissed

    # Admin-side notes (never shown to reporter directly to prevent info leakage)
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Severity assessment
    severity: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    # Severity: low, medium, high, critical
