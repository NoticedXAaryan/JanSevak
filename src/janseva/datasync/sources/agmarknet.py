import httpx
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from janseva.datasync.base import DataSource
from janseva.db.models.mandi_price import MandiPrice

class AgmarknetSource(DataSource):
    """
    Data source for Mandi prices via data.gov.in (Agmarknet).
    Note: We'll use a mocked fetch here for the hackathon, but structure it properly.
    """
    
    def __init__(self):
        super().__init__(name="agmarknet")
        
    async def fetch_latest(self) -> List[Dict[str, Any]]:
        """
        In a real scenario, this would call data.gov.in APIs or the CEDA Agmarknet API.
        For demonstration, we mock some updated data.
        """
        # TODO: Implement actual API call
        # e.g. async with httpx.AsyncClient() as client:
        #          resp = await client.get("https://api.data.gov.in/resource/...", params={"api-key": "..."})
        #          return resp.json()["records"]
        
        today = datetime.now().date()
        mock_data = [
            {
                "state": "Madhya Pradesh",
                "district": "Indore",
                "market": "Indore",
                "commodity": "Wheat",
                "variety": "Lokwan",
                "grade": "FAQ",
                "min_price": 2200.0,
                "max_price": 2400.0,
                "modal_price": 2300.0,
                "price_date": today,
            },
            {
                "state": "Madhya Pradesh",
                "district": "Indore",
                "market": "Indore",
                "commodity": "Soyabean",
                "variety": "Yellow",
                "grade": "FAQ",
                "min_price": 4200.0,
                "max_price": 4500.0,
                "modal_price": 4400.0,
                "price_date": today,
            }
        ]
        return mock_data

    async def sync_to_db(self, session: AsyncSession, data: List[Dict[str, Any]]) -> int:
        synced_count = 0
        now = datetime.now()
        
        for record in data:
            # Upsert logic based on state/district/market/commodity/date
            stmt = select(MandiPrice).where(
                MandiPrice.state == record["state"],
                MandiPrice.district == record["district"],
                MandiPrice.market_name == record["market"],
                MandiPrice.crop_name == record["commodity"],
                MandiPrice.date == record["price_date"]
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                existing.min_price = record["min_price"]
                existing.max_price = record["max_price"]
                existing.modal_price = record["modal_price"]
                existing.last_synced_at = now
            else:
                new_price = MandiPrice(
                    state=record["state"],
                    district=record["district"],
                    market_name=record["market"],
                    crop_name=record["commodity"],
                    variety=record.get("variety"),
                    grade=record.get("grade"),
                    min_price=record["min_price"],
                    max_price=record["max_price"],
                    modal_price=record["modal_price"],
                    date=record["price_date"],
                    source_api="agmarknet",
                    last_synced_at=now
                )
                session.add(new_price)
            synced_count += 1
            
        return synced_count
