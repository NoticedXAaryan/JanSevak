"""Reports API for JanSevak v2 (Whistleblowing / Sealed Envelope)."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
import uuid
import secrets
import string

from janseva.db.engine import async_session_factory
from janseva.db.models.anonymous_report import AnonymousReport

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])

# --- Schemas ---
class ReportCreateRequest(BaseModel):
    category: str
    content_encrypted: str
    district: str | None = None
    state: str | None = None
    identity_envelope_encrypted: str
    evidence_image_urls: list[str] | None = None

class SealedEnvelopeUnlockRequest(BaseModel):
    token: str
    key_fragment_1: str
    key_fragment_2: str

# --- Endpoints ---
@router.post("")
async def create_report(req: ReportCreateRequest):
    """Submit an anonymous report with a sealed identity envelope."""
    async with async_session_factory() as session:
        # Generate tracking token (e.g., K7M2-P9X4-R1N6)
        alphabet = string.ascii_uppercase + string.digits
        token = '-'.join([''.join(secrets.choice(alphabet) for i in range(4)) for _ in range(3)])
        
        report = AnonymousReport(
            report_token=token,
            category=req.category,
            content_encrypted=req.content_encrypted,
            district=req.district,
            state=req.state,
            identity_envelope_encrypted=req.identity_envelope_encrypted,
            evidence_image_urls=req.evidence_image_urls,
            status="submitted"
        )
        session.add(report)
        await session.commit()
        return {"status": "success", "report_token": token}

@router.get("/{token}")
async def get_report_status(token: str):
    """Check report status using tracking token."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(AnonymousReport).where(AnonymousReport.report_token == token)
        )
        report = result.scalar_one_or_none()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
            
        return {
            "status": report.status,
            "category": report.category,
            "created_at": report.created_at.isoformat()
            # Do NOT return encrypted content or envelope to prevent leak
        }

@router.post("/{token}/unseal")
async def unseal_identity(token: str, req: SealedEnvelopeUnlockRequest):
    """
    Attempt to unseal the identity envelope using two key fragments.
    This simulates a legal order execution.
    """
    # In a real implementation:
    # 1. Validate both keys against their respective authorities
    # 2. Reconstruct the symmetric key
    # 3. Decrypt req.identity_envelope_encrypted
    # 4. Log this highly sensitive action in AuditLog
    
    return {"status": "error", "message": "Unsealing requires court order and dual-key auth (Not implemented in demo)"}
