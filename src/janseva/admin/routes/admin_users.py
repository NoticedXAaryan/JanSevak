from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import uuid

from janseva.admin.auth import get_current_admin
from janseva.admin.app import templates
from janseva.db.engine import get_session
from janseva.db.models.admin_user import AdminUser
from janseva.db.models.organization import Organization

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def list_admin_users(
    request: Request,
    admin_user: dict = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session)
):
    """List all admin users (Super Admin only)."""
    if admin_user["role"] != "super_admin":
        return HTMLResponse(content="Unauthorized", status_code=403)
        
    stmt = select(AdminUser).options(selectinload(AdminUser.organization)).order_by(AdminUser.created_at.desc())
    result = await session.execute(stmt)
    users = result.scalars().all()
    
    # Get orgs for the dropdown
    orgs_stmt = select(Organization).order_by(Organization.name)
    orgs_result = await session.execute(orgs_stmt)
    orgs = orgs_result.scalars().all()

    return templates.TemplateResponse(request=request, name="admin_users.html", context={
            "request": request,
            "admin": admin_user,
            "users": users,
            "organizations": orgs,
        })

@router.post("/create")
async def create_admin_user(
    email: str = Form(...),
    full_name: str = Form(...),
    role: str = Form(...),
    org_id: str = Form(""),
    admin_user: dict = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session)
):
    """Create a new admin user."""
    if admin_user["role"] != "super_admin":
        return HTMLResponse(content="Unauthorized", status_code=403)
        
    # Pre-provision the user. They will login with Google OAuth via this email later.
    new_user = AdminUser(
        email=email,
        full_name=full_name,
        role=role,
        organization_id=uuid.UUID(org_id) if org_id else None
    )
    session.add(new_user)
    await session.commit()
    
    # Reload page
    return RedirectResponse(url="/admin/users", status_code=303)
