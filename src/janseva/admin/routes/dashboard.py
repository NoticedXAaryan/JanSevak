from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from janseva.admin.auth import get_current_admin

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
from janseva.db.engine import get_session
from janseva.db.models.anonymous_report import AnonymousReport
from janseva.db.models.conversation import Conversation
from janseva.db.models.user import User

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard_home(
    request: Request,
    admin_user: dict = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
):
    """Dashboard home with stats."""

    # 1. Total Users (Super Admin only for now)
    users_count = (
        await session.scalar(select(func.count()).select_from(User))
        if admin_user["role"] == "super_admin"
        else 0
    )

    # 2. Total Conversations (Super Admin only for now)
    conversations_count = (
        await session.scalar(select(func.count()).select_from(Conversation))
        if admin_user["role"] == "super_admin"
        else 0
    )

    # 3. Active Escalations (Not yet implemented, just a placeholder)
    escalations_count = 0

    # 4. Pending Reports
    reports_query = (
        select(func.count()).select_from(AnonymousReport).where(AnonymousReport.status == "pending")
    )
    if admin_user["role"] != "super_admin":
        if admin_user.get("org_id"):
            reports_query = reports_query.where(
                AnonymousReport.organization_id == admin_user["org_id"]
            )
        else:
            # No org assigned -> no reports
            reports_query = None

    reports_count = await session.scalar(reports_query) if reports_query is not None else 0

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "admin": admin_user,
            "stats": {
                "users": users_count or 0,
                "conversations": conversations_count or 0,
                "escalations": escalations_count,
                "pending_reports": reports_count or 0,
            },
        },
    )
