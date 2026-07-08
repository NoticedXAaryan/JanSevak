"""
Seed the authority hierarchy database.
This is sample data — customize for your target district/state.

Run: uv run python scripts/seed_authorities.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from janseva.common.logging import setup_logging
from janseva.db.engine import async_session_factory
from janseva.db.models.authority import Authority

SAMPLE_HIERARCHY = [
    # Level 5: State Level
    {
        "title": "Director General of Police (DGP)",
        "title_hi": "पुलिस महानिदेशक",
        "department": "Police",
        "level": 5,
        "state": "Sample State",
    },
    {
        "title": "Chief Secretary",
        "title_hi": "मुख्य सचिव",
        "department": "General Administration",
        "level": 5,
        "state": "Sample State",
    },
    # Level 4: Division Level
    {
        "title": "Inspector General of Police (IG)",
        "title_hi": "पुलिस महानिरीक्षक",
        "department": "Police",
        "level": 4,
        "state": "Sample State",
    },
    {
        "title": "Divisional Commissioner",
        "title_hi": "मंडलायुक्त",
        "department": "Revenue",
        "level": 4,
        "state": "Sample State",
    },
    # Level 3: District Level
    {
        "title": "Superintendent of Police (SP)",
        "title_hi": "पुलिस अधीक्षक",
        "department": "Police",
        "level": 3,
        "district": "Sample District",
    },
    {
        "title": "District Magistrate (DM)",
        "title_hi": "जिलाधिकारी",
        "department": "Revenue",
        "level": 3,
        "district": "Sample District",
    },
    {
        "title": "Chief Medical Officer (CMO)",
        "title_hi": "मुख्य चिकित्साधिकारी",
        "department": "Health",
        "level": 3,
        "district": "Sample District",
    },
    # Level 2: Block Level
    {
        "title": "Station House Officer (SHO)",
        "title_hi": "थाना प्रभारी",
        "department": "Police",
        "level": 2,
        "district": "Sample District",
    },
    {
        "title": "Block Development Officer (BDO)",
        "title_hi": "खंड विकास अधिकारी",
        "department": "Revenue",
        "level": 2,
        "district": "Sample District",
    },
    {
        "title": "Tehsildar",
        "title_hi": "तहसीलदार",
        "department": "Revenue",
        "level": 2,
        "district": "Sample District",
    },
    # Level 1: Village Level
    {
        "title": "Village Pradhan / Sarpanch",
        "title_hi": "ग्राम प्रधान / सरपंच",
        "department": "Panchayati Raj",
        "level": 1,
        "district": "Sample District",
    },
    {
        "title": "Gram Panchayat Secretary",
        "title_hi": "ग्राम पंचायत सचिव",
        "department": "Panchayati Raj",
        "level": 1,
        "district": "Sample District",
    },
    {
        "title": "Patwari / Lekhpal",
        "title_hi": "पटवारी / लेखपाल",
        "department": "Revenue",
        "level": 1,
        "district": "Sample District",
    },
]


async def seed():
    setup_logging()
    async with async_session_factory() as session:
        for data in SAMPLE_HIERARCHY:
            authority = Authority(**data)
            session.add(authority)
        await session.commit()
        print(f"✅ Seeded {len(SAMPLE_HIERARCHY)} authorities.")


if __name__ == "__main__":
    asyncio.run(seed())
