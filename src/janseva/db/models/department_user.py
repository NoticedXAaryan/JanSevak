"""DepartmentUser model — represents a government official account."""
import uuid
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class DepartmentUser(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "department_users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    full_name: Mapped[str] = mapped_column(String(500), nullable=False)
    designation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False
    )
    
    role: Mapped[str] = mapped_column(String(50), default="dept_viewer", nullable=False)
    # "dept_admin" | "dept_editor" | "dept_viewer"
    
    is_primary_contact: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    department = relationship("Department", back_populates="department_users")
