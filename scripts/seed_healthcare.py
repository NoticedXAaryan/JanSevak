"""Seed script for Healthcare Facilities."""
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from janseva.config import settings
from janseva.db.models.healthcare_facility import HealthcareFacility


async def seed_healthcare_facilities():
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    facilities = [
        # Bhopal
        HealthcareFacility(
            name="Hamidia Hospital",
            name_hi="हमीदिया अस्पताल",
            facility_type="government_hospital",
            district="Bhopal",
            state="Madhya Pradesh",
            address="Royal Market, Bhopal",
            specialties=["general", "orthopedics", "pediatrics", "ophthalmology", "cardiology"],
            total_beds=1200,
            available_beds=45,
            is_accepting_patients=True,
            phone="0755-2540590",
        ),
        HealthcareFacility(
            name="JP Hospital",
            name_hi="जेपी अस्पताल",
            facility_type="government_hospital",
            district="Bhopal",
            state="Madhya Pradesh",
            address="Link Road No 1, TT Nagar, Bhopal",
            specialties=["general", "gynecology", "pediatrics", "dentistry"],
            total_beds=500,
            available_beds=12,
            is_accepting_patients=True,
            phone="0755-2550100",
        ),
        HealthcareFacility(
            name="AIIMS Bhopal",
            name_hi="एम्स भोपाल",
            facility_type="government_hospital",
            district="Bhopal",
            state="Madhya Pradesh",
            address="Saket Nagar, Bhopal",
            specialties=["general", "neurology", "oncology", "cardiology", "nephrology"],
            total_beds=960,
            available_beds=0, # Fully occupied
            is_accepting_patients=False,
            phone="0755-2672322",
        ),
        HealthcareFacility(
            name="Bairagarh CHC",
            name_hi="बैरागढ़ सामुदायिक स्वास्थ्य केंद्र",
            facility_type="CHC",
            district="Bhopal",
            state="Madhya Pradesh",
            address="Bairagarh, Bhopal",
            specialties=["general", "maternity"],
            total_beds=30,
            available_beds=5,
            is_accepting_patients=True,
        ),
        # Indore
        HealthcareFacility(
            name="MY Hospital",
            name_hi="एमवाय अस्पताल",
            facility_type="government_hospital",
            district="Indore",
            state="Madhya Pradesh",
            address="MTH Compound, Indore",
            specialties=["general", "surgery", "orthopedics", "pediatrics", "ophthalmology"],
            total_beds=1400,
            available_beds=150,
            is_accepting_patients=True,
        ),
        # Delhi
        HealthcareFacility(
            name="Safdarjung Hospital",
            name_hi="सफदरजंग अस्पताल",
            facility_type="government_hospital",
            district="New Delhi",
            state="Delhi",
            address="Ansari Nagar East, New Delhi",
            specialties=["general", "burns", "orthopedics", "cardiology"],
            total_beds=2900,
            available_beds=85,
            is_accepting_patients=True,
        )
    ]
    
    async with async_session() as session:
        # Check if already seeded
        from sqlalchemy import select
        existing = await session.execute(select(HealthcareFacility).limit(1))
        if existing.scalar_one_or_none():
            print("Healthcare facilities already seeded. Skipping.")
            return

        session.add_all(facilities)
        await session.commit()
        print(f"Seeded {len(facilities)} healthcare facilities successfully.")

if __name__ == "__main__":
    # Ensure event loop handles it
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_healthcare_facilities())
