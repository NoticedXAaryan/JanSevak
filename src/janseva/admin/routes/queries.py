from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from janseva.admin.auth import get_current_admin
from janseva.admin.app import templates
from janseva.db.engine import get_session
from janseva.db.models.message import Message

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def list_queries(
    request: Request,
    admin_user: dict = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session)
):
    """List recent user messages/queries."""
    if admin_user["role"] == "super_admin":
        # Fetch latest 20 user messages
        stmt = select(Message).where(Message.role == "user").order_by(Message.created_at.desc()).limit(20)
        result = await session.execute(stmt)
        queries = result.scalars().all()
    else:
        # Queries are global right now, non-super admins shouldn't see them
        queries = []

    return templates.TemplateResponse(
        "queries.html",
        {
            "request": request,
            "admin": admin_user,
            "queries": queries,
        }
    )
