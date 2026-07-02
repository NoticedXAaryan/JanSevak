# Guide 09: Healthcare Agent

## What This Does
Adds a specialist agent for healthcare queries — finding nearby hospitals, checking availability, and booking appointments.

## Prerequisites
- Guide 03 completed (AI agent core)
- Guide 04 completed (knowledge base system — we'll use it for healthcare facility data)

---

## Overview

The Healthcare Agent handles:
1. "Find me a nearby hospital" → Searches facility database by district + specialty
2. "I need an eye checkup" → Finds ophthalmology departments, checks availability
3. "Book an appointment" → Generates queue number, estimated wait time
4. "Is the government hospital busy?" → Checks simulated capacity data

## Data Model

**File: `src/janseva/db/models/healthcare_facility.py`** (new model)

```python
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
```

## Implementation Steps

1. Create the healthcare facility model + migration
2. Create healthcare facility seed data (YAML or seed script)
3. Build the Healthcare Agent as a LangGraph specialist
4. Implement facility search tool (filter by district + specialty + availability)
5. Implement appointment booking flow (generate queue number)
6. Wire into the orchestrator

## Healthcare Agent System Prompt

The agent should:
- Search facilities by district and specialty
- Show availability status
- Generate queue numbers (simple incrementing ID per facility per day)
- Suggest alternatives if primary facility is busy
- Respond in user's language

---

## Git Checkpoint
```bash
git add -A
git commit -m "feat(healthcare): implement healthcare facility search and booking agent"
```
