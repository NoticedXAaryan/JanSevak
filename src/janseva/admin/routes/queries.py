from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from janseva.admin.auth import get_current_admin
from janseva.admin.app import templates
from janseva.db.engine import get_async_session
from janseva.db.models.message import Message

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def list_queries(
    request: Request,
    admin_username: str = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """List recent user messages/queries."""
    # Fetch latest 20 user messages
    stmt = select(Message).where(Message.role == "user").order_by(Message.created_at.desc()).limit(20)
    result = await session.execute(stmt)
    queries = result.scalars().all()

    return templates.TemplateResponse(
        "queries.html",
        {
            "request": request,
            "admin": admin_username,
            "queries": queries,
        }
    )
