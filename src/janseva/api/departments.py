"""Departments API for JanSevak v2."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
import uuid

from janseva.db.engine import async_session_factory
from janseva.db.models.department import Department
from janseva.db.models.public_complaint import PublicComplaint
from janseva.db.models.anonymous_report import AnonymousReport

router = APIRouter(prefix="/api/v1/departments", tags=["departments"])

# --- Schemas ---
class PolicyUpdate(BaseModel):
    policies_json: dict

# --- Endpoints ---
@router.get("")
async def list_departments():
    """List all departments."""
    async with async_session_factory() as session:
        result = await session.execute(select(Department))
        departments = result.scalars().all()
        return [
            {
                "id": str(d.id),
                "name": d.name,
                "type": d.department_type,
                "district": d.jurisdiction_district
            } for d in departments
        ]

@router.get("/{id}")
async def get_department(id: uuid.UUID):
    """Get department details."""
    async with async_session_factory() as session:
        result = await session.execute(select(Department).where(Department.id == id))
        dept = result.scalar_one_or_none()
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
            
        return {
            "id": str(dept.id),
            "name": dept.name,
            "policies": dept.policies_json
        }

@router.patch("/{id}/policies")
async def update_policies(id: uuid.UUID, req: PolicyUpdate):
    """Update department policies."""
    async with async_session_factory() as session:
        result = await session.execute(select(Department).where(Department.id == id))
        dept = result.scalar_one_or_none()
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
            
        dept.policies_json = req.policies_json
        await session.commit()
        return {"status": "success"}

@router.get("/{id}/complaints")
async def get_dept_complaints(id: uuid.UUID):
    """Get complaints assigned to a department."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(PublicComplaint).where(PublicComplaint.assigned_department_id == id)
        )
        return [{"id": str(c.id), "status": c.status} for c in result.scalars().all()]
