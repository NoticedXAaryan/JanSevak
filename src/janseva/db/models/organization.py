"""Organization model — represents a government authority entity."""
import uuid
from sqlalchemy import String, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Organization(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    org_type: Mapped[str] = mapped_column(String(50), nullable=False) # "hospital" | "police_station" | "fire_station" | "panchayat" | "district_office" | "tehsil"
    jurisdiction_state: Mapped[str] = mapped_column(String(255), nullable=False)
    jurisdiction_district: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    jurisdiction_block: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    admin_users = relationship("AdminUser", back_populates="organization")
