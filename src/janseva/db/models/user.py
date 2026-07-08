"""User model — represents a citizen using JanSeva."""

from sqlalchemy import BigInteger, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    # Identifiers & Auth
    auth_provider: Mapped[str] = mapped_column(
        String(50), default="telegram", nullable=False
    )  # "telegram", "phone", "email"
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger, unique=True, nullable=True, index=True
    )
    telegram_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(
        String(50), unique=True, nullable=True, index=True
    )
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True, index=True)

    # Personal Info
    full_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(10), default="hi", nullable=False)

    # Location
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)
    district: Mapped[str | None] = mapped_column(String(255), nullable=True)
    block: Mapped[str | None] = mapped_column(String(255), nullable=True)
    pin_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Preferences
    interests: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    notifications_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    onboarding_complete: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relationships
    conversations = relationship("Conversation", back_populates="user", lazy="selectin")
