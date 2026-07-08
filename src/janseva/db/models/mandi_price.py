"""Mandi (Wholesale Market) Price model."""

import datetime

from sqlalchemy import Date, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class MandiPrice(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mandi_prices"

    crop_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    crop_name_hi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    variety: Mapped[str | None] = mapped_column(String(255), nullable=True)
    grade: Mapped[str | None] = mapped_column(String(100), nullable=True)

    state: Mapped[str] = mapped_column(String(255), nullable=False)
    district: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    market_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Prices in INR per Quintal (100 kg)
    min_price: Mapped[float] = mapped_column(Float, nullable=False)
    max_price: Mapped[float] = mapped_column(Float, nullable=False)
    modal_price: Mapped[float] = mapped_column(Float, nullable=False)

    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    source_api: Mapped[str | None] = mapped_column(String(255), default="agmarknet")
    last_synced_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
