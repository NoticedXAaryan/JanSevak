"""Healthcare facility model."""
from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class HealthcareFacility(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "healthcare_facilities"

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    name_hi: Mapped[str | None] = mapped_column(String(500), nullable=True)
    facility_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # Types: government_hospital, CHC, PHC, private_hospital, clinic
    
    district: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    specialties: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    # e.g., ["general", "ophthalmology", "orthopedics", "gynecology"]
    
    total_beds: Mapped[int] = mapped_column(Integer, default=0)
    available_beds: Mapped[int] = mapped_column(Integer, default=0)
    
    is_accepting_patients: Mapped[bool] = mapped_column(Boolean, default=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
