"""Seed script for Mandi Prices."""

import asyncio
import datetime
import sys

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from janseva.config import settings
from janseva.db.models.mandi_price import MandiPrice


async def seed_mandi_prices():
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    today = datetime.date.today()

    prices = [
        # Bhopal - Wheat
        MandiPrice(
            crop_name="Wheat",
            crop_name_hi="गेहूँ",
            state="Madhya Pradesh",
            district="Bhopal",
            market_name="Karond Mandi",
            min_price=2200.0,
            max_price=2450.0,
            modal_price=2300.0,
            date=today,
        ),
        # Bhopal - Rice
        MandiPrice(
            crop_name="Rice",
            crop_name_hi="चावल",
            state="Madhya Pradesh",
            district="Bhopal",
            market_name="Karond Mandi",
            min_price=2800.0,
            max_price=3500.0,
            modal_price=3100.0,
            date=today,
        ),
        # Indore - Soybean
        MandiPrice(
            crop_name="Soybean",
            crop_name_hi="सोयाबीन",
            state="Madhya Pradesh",
            district="Indore",
            market_name="Laxmibai Nagar Mandi",
            min_price=4100.0,
            max_price=4800.0,
            modal_price=4500.0,
            date=today,
        ),
        # Indore - Wheat
        MandiPrice(
            crop_name="Wheat",
            crop_name_hi="गेहूँ",
            state="Madhya Pradesh",
            district="Indore",
            market_name="Chhawani Mandi",
            min_price=2150.0,
            max_price=2500.0,
            modal_price=2350.0,
            date=today,
        ),
        # Delhi - Onion
        MandiPrice(
            crop_name="Onion",
            crop_name_hi="प्याज",
            state="Delhi",
            district="New Delhi",
            market_name="Azadpur Mandi",
            min_price=1200.0,
            max_price=2200.0,
            modal_price=1800.0,
            date=today,
        ),
    ]

    async with async_session() as session:
        # Check if already seeded
        from sqlalchemy import select

        existing = await session.execute(
            select(MandiPrice).where(MandiPrice.date == today).limit(1)
        )
        if existing.scalar_one_or_none():
            print("Mandi prices for today already seeded. Skipping.")
            return

        session.add_all(prices)
        await session.commit()
        print(f"Seeded {len(prices)} mandi prices successfully for {today}.")


if __name__ == "__main__":
    # Ensure event loop handles it
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_mandi_prices())
