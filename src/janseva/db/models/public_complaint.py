"""PublicComplaint model — represents non-anonymous issues reported by citizens."""

import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class PublicComplaint(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "public_complaints"

    complaint_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    # E.g., "CMP-2026-0001"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    category: Mapped[str] = mapped_column(String(100), nullable=False)
    # pothole, water_supply, garbage, street_light, drainage, road_damage, encroachment, noise, other

    description: Mapped[str] = mapped_column(Text, nullable=False)
    location_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    image_urls: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    status: Mapped[str] = mapped_column(String(50), default="submitted", nullable=False, index=True)
    # submitted, acknowledged, in_progress, resolved, rejected

    assigned_department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True, index=True
    )

    priority: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    # low, medium, high, urgent

    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", backref="complaints")
    assigned_department = relationship("Department", backref="complaints")
