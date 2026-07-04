import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from janseva.config import settings

# In a real app, use bcrypt. For the hackathon, we'll just check against the plain text in .env
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login", auto_error=False)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.admin_jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, correct_password: str) -> bool:
    # Hackathon simplicity: raw password check against .env
    return plain_password == correct_password


async def get_current_admin(request: Request) -> dict:
    """
    Dependency to get the current admin from the JWT token in cookies.
    Returns a dict with user details (sub/email, role, org_id).
    """
    token = request.cookies.get("admin_token")
    if not token:
        # Fallback to header if needed
        token = await oauth2_scheme(request)
        
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(token, settings.admin_jwt_secret, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
        return {
            "email": email,
            "role": payload.get("role", "super_admin" if email == settings.admin_username else "org_viewer"),
            "org_id": payload.get("org_id")
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_admin_optional(request: Request) -> Optional[dict]:
    """Optional auth check, doesn't raise exception if not logged in."""
    token = request.cookies.get("admin_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.admin_jwt_secret, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email:
            return {
                "email": email,
                "role": payload.get("role", "super_admin" if email == settings.admin_username else "org_viewer"),
                "org_id": payload.get("org_id")
            }
    except JWTError:
        pass
    return None
