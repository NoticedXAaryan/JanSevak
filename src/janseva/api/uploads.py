"""Uploads API for JanSevak v2."""

import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/api/v1/uploads", tags=["uploads"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image file (e.g., pothole photo)."""
    content_type = file.content_type or ""
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    safe_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = UPLOAD_DIR / safe_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # In production, upload to S3 and return CDN URL
    # For demo, return local path relative to static mount
    return {"status": "success", "url": f"/static/uploads/{safe_filename}"}
