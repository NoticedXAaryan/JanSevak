from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from sqlalchemy import text

from janseva.agents.llm import get_llm
from janseva.config import settings
from janseva.db.engine import async_session_factory

router = APIRouter(tags=["Diagnostics"])

class DiagnosticResponse(BaseModel):
    status: str
    database: str
    llm: str
    llm_response: str | None
    provider: str
    model: str
    error: str | None = None

@router.get("/diagnostics/test", response_model=DiagnosticResponse)
async def run_diagnostics():
    """Run full system diagnostics to verify database and LLM connectivity."""
    db_status = "unknown"
    llm_status = "unknown"
    llm_response_text = None
    error_msg = None

    # Test Database
    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = "failed"
        error_msg = f"DB Error: {str(e)}"

    # Test LLM
    try:
        llm = get_llm()
        msg = HumanMessage(content="Hello! Reply exactly with 'Connection Successful'.")
        response = await llm.ainvoke([msg])
        llm_status = "connected"
        llm_response_text = response.content
    except Exception as e:
        llm_status = "failed"
        error_msg = f"{error_msg} | " if error_msg else ""
        error_msg += f"LLM Error: {str(e)}"

    overall_status = "ok" if db_status == "connected" and llm_status == "connected" else "error"

    return DiagnosticResponse(
        status=overall_status,
        database=db_status,
        llm=llm_status,
        llm_response=llm_response_text,
        provider=settings.llm_provider,
        model=settings.llm_model,
        error=error_msg
    )
