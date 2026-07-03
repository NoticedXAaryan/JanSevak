"""
Authority hierarchy model.
Represents the chain of command in government bodies.
Used to route anonymous reports to the correct superior.
"""
import uuid
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Authority(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "authorities"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    title_hi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    district: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    # Level hierarchy (higher = more authority):
    # 1 = Village level (Gram Pradhan, local constable)
    # 2 = Block/Tehsil level (BDO, SHO)
    # 3 = District level (DM, SP)
    # 4 = Division level (Commissioner, DIG)
    # 5 = State level (Chief Secretary, DGP)

    reports_to_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("authorities.id"), nullable=True
    )

    # Self-referential relationship
    reports_to = relationship("Authority", remote_side="Authority.id", lazy="selectin")
