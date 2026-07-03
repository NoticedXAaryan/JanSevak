from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from janseva.admin.auth import get_current_admin
from janseva.admin.app import templates
from janseva.db.engine import get_async_session
from janseva.db.models.user import User
from janseva.db.models.conversation import Conversation
from janseva.db.models.anonymous_report import AnonymousReport

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(
    request: Request,
    admin_username: str = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """Dashboard home with stats."""
    
    # 1. Total Users
    users_count = await session.scalar(select(func.count()).select_from(User))
    
    # 2. Total Conversations
    conversations_count = await session.scalar(select(func.count()).select_from(Conversation))
    
    # 3. Active Escalations (Not yet implemented, just a placeholder)
    escalations_count = 0
    
    # 4. Pending Reports
    reports_count = await session.scalar(
        select(func.count()).select_from(AnonymousReport).where(AnonymousReport.status == "pending")
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "admin": admin_username,
            "stats": {
                "users": users_count or 0,
                "conversations": conversations_count or 0,
                "escalations": escalations_count,
                "pending_reports": reports_count or 0,
            }
        }
    )
