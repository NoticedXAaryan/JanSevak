"""Department model — represents a government authority entity."""
import uuid
from sqlalchemy import String, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Department(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name_hi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    code: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True)
    department_type: Mapped[str] = mapped_column(String(50), nullable=False) 
    # "revenue" | "police" | "health" | "education" | "agriculture" | "municipal" | "panchayat" | "welfare"

    jurisdiction_state: Mapped[str] = mapped_column(String(255), nullable=False)
    jurisdiction_district: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    jurisdiction_block: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    office_address: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    policies_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    onboarding_complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    department_users = relationship("DepartmentUser", back_populates="department")
