"""Complaints API for JanSevak v2."""

import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from janseva.db.engine import async_session_factory
from janseva.db.models.public_complaint import PublicComplaint

router = APIRouter(prefix="/api/v1/complaints", tags=["complaints"])


# --- Schemas ---
class ComplaintCreateRequest(BaseModel):
    user_id: uuid.UUID
    category: str
    description: str
    location_text: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    image_urls: list[str] | None = None


class ComplaintStatusUpdate(BaseModel):
    status: str
    resolution_notes: str | None = None


# --- Endpoints ---
@router.post("")
async def create_complaint(req: ComplaintCreateRequest):
    """Submit a public complaint."""
    async with async_session_factory() as session:
        # Generate readable ID
        year = datetime.now().year
        # In a real app, use a sequence. Mocking for now:
        complaint_id = f"CMP-{year}-{str(uuid.uuid4())[:6].upper()}"

        complaint = PublicComplaint(
            complaint_id=complaint_id,
            user_id=req.user_id,
            category=req.category,
            description=req.description,
            location_text=req.location_text,
            latitude=req.latitude,
            longitude=req.longitude,
            image_urls=req.image_urls,
            status="submitted",
        )
        session.add(complaint)
        await session.commit()
        return {"status": "success", "complaint_id": complaint_id, "id": str(complaint.id)}


@router.get("/{complaint_id}")
async def get_complaint(complaint_id: str):
    """Get complaint by readable ID."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(PublicComplaint).where(PublicComplaint.complaint_id == complaint_id)
        )
        complaint = result.scalar_one_or_none()
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        return {
            "id": str(complaint.id),
            "complaint_id": complaint.complaint_id,
            "category": complaint.category,
            "status": complaint.status,
            "description": complaint.description,
            "resolution_notes": complaint.resolution_notes,
            "created_at": complaint.created_at.isoformat(),
        }


@router.patch("/{id}/status")
async def update_complaint_status(id: uuid.UUID, req: ComplaintStatusUpdate):
    """Department updates complaint status."""
    async with async_session_factory() as session:
        result = await session.execute(select(PublicComplaint).where(PublicComplaint.id == id))
        complaint = result.scalar_one_or_none()
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        complaint.status = req.status
        if req.resolution_notes:
            complaint.resolution_notes = req.resolution_notes

        if req.status == "resolved":
            complaint.resolved_at = datetime.now()

        await session.commit()
        return {"status": "success"}
