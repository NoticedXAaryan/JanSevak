from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from janseva.admin.auth import get_current_admin
from fastapi.templating import Jinja2Templates
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
from janseva.db.engine import get_session
from janseva.db.models.anonymous_report import AnonymousReport

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def list_reports(
    request: Request,
    admin_user: dict = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session)
):
    """List anonymous reports."""
    # Scope reports to organization unless super_admin
    if admin_user["role"] == "super_admin":
        stmt = select(AnonymousReport).order_by(AnonymousReport.created_at.desc())
    else:
        # Fallback to empty if no org_id assigned
        org_id = admin_user.get("org_id")
        if not org_id:
            return templates.TemplateResponse(request=request, name="reports.html", context={"request": request, "admin": admin_user, "reports": []})
        
        stmt = select(AnonymousReport).where(
            AnonymousReport.organization_id == org_id
        ).order_by(AnonymousReport.created_at.desc())
        
    result = await session.execute(stmt)
    reports = result.scalars().all()

    return templates.TemplateResponse(request=request, name="reports.html", context={
            "request": request,
            "admin": admin_user,
            "reports": reports,
        })

@router.post("/{report_id}/status")
async def update_report_status(
    report_id: str,
    status: str = Form(...),
    admin_user: dict = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session)
):
    """Update report status."""
    # Build base update statement
    stmt = update(AnonymousReport).where(
        AnonymousReport.id == uuid.UUID(report_id)
    )
    
    # Enforce org scope for non-super admins
    if admin_user["role"] != "super_admin":
        org_id = admin_user.get("org_id")
        if not org_id:
            return HTMLResponse(content="<span class='text-red-500'>Unauthorized</span>", status_code=403)
        stmt = stmt.where(AnonymousReport.organization_id == org_id)
        
    stmt = stmt.values(status=status)
    
    await session.execute(stmt)
    await session.commit()
    
    # Return HTML for HTMX to swap just the status badge or we can just redirect/reload
    # To keep it simple, we'll reload the row or just return a simple success and reload page
    return HTMLResponse(
        content=f"<span class='text-sm text-green-600'>Status updated to {status}</span>",
        status_code=200
    )
