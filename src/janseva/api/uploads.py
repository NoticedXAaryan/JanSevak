"""Uploads API for JanSevak v2."""
from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/api/v1/uploads", tags=["uploads"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image file (e.g., pothole photo)."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
        
    # Generate safe filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    safe_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = UPLOAD_DIR / safe_filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # In production, upload to S3 and return CDN URL
    # For demo, return local path relative to static mount
    return {"status": "success", "url": f"/static/uploads/{safe_filename}"}
