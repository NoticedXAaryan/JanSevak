from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from janseva.admin.auth import get_current_admin
from janseva.admin.app import templates
from janseva.db.engine import get_session
from janseva.db.models.organization import Organization

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def list_organizations(
    request: Request,
    admin_user: dict = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session)
):
    """List all organizations (Super Admin only)."""
    if admin_user["role"] != "super_admin":
        return HTMLResponse(content="Unauthorized", status_code=403)
        
    stmt = select(Organization).order_by(Organization.created_at.desc())
    result = await session.execute(stmt)
    orgs = result.scalars().all()

    return templates.TemplateResponse(request=request, name="organizations.html", context={
            "request": request,
            "admin": admin_user,
            "organizations": orgs,
        })

@router.post("/create")
async def create_organization(
    name: str = Form(...),
    org_type: str = Form(...),
    state: str = Form(...),
    district: str = Form(...),
    admin_user: dict = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session)
):
    """Create a new organization."""
    if admin_user["role"] != "super_admin":
        return HTMLResponse(content="Unauthorized", status_code=403)
        
    org = Organization(
        name=name,
        org_type=org_type,
        jurisdiction_state=state,
        jurisdiction_district=district,
    )
    session.add(org)
    await session.commit()
    
    # Reload page
    return RedirectResponse(url="/admin/organizations", status_code=303)
