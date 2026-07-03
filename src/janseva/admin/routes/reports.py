from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from janseva.admin.auth import get_current_admin
from janseva.admin.app import templates
from janseva.db.engine import get_async_session
from janseva.db.models.anonymous_report import AnonymousReport

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def list_reports(
    request: Request,
    admin_username: str = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """List anonymous reports."""
    stmt = select(AnonymousReport).order_by(AnonymousReport.created_at.desc())
    result = await session.execute(stmt)
    reports = result.scalars().all()

    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "admin": admin_username,
            "reports": reports,
        }
    )

@router.post("/{report_id}/status")
async def update_report_status(
    report_id: str,
    status: str = Form(...),
    admin_username: str = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """Update report status."""
    stmt = update(AnonymousReport).where(
        AnonymousReport.id == uuid.UUID(report_id)
    ).values(status=status)
    
    await session.execute(stmt)
    await session.commit()
    
    # Return HTML for HTMX to swap just the status badge or we can just redirect/reload
    # To keep it simple, we'll reload the row or just return a simple success and reload page
    return HTMLResponse(
        content=f"<span class='text-sm text-green-600'>Status updated to {status}</span>",
        status_code=200
    )
