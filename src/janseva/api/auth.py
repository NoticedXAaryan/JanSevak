"""Authentication API for JanSevak v2."""

import uuid
from datetime import UTC, datetime, timedelta

from aiogram import Bot
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from janseva.common.cache import query_cache
from janseva.config import settings
from janseva.db.engine import async_session_factory
from janseva.db.models.department_user import DepartmentUser
from janseva.db.models.user import User
from janseva.notifications.engine import send_notification

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/dept/login")


# Initialize bot lazily
def get_bot():
    return Bot(token=settings.telegram_bot_token)


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# --- Schemas ---
class CitizenRegisterRequest(BaseModel):
    phone_number: str
    full_name: str
    pin_code: str | None = None
    state: str | None = None
    district: str | None = None


class OTPRequest(BaseModel):
    phone_number: str


class CitizenLoginRequest(BaseModel):
    phone_number: str
    otp: str


class DeptRegisterRequest(BaseModel):
    department_id: uuid.UUID
    email: EmailStr
    full_name: str
    password: str
    designation: str | None = None


class DeptLoginRequest(BaseModel):
    email: EmailStr
    password: str


# --- Endpoints ---
@router.post("/register")
async def register_citizen(req: CitizenRegisterRequest):
    """Register a new citizen via phone number."""
    async with async_session_factory() as session:
        # Check if exists
        result = await session.execute(select(User).where(User.phone_number == req.phone_number))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Phone number already registered")

        # Create user
        user = User(
            auth_provider="phone",
            phone_number=req.phone_number,
            full_name=req.full_name,
            pin_code=req.pin_code,
            state=req.state,
            district=req.district,
        )
        session.add(user)
        await session.commit()
        return {"status": "success", "user_id": str(user.id)}


@router.post("/otp/request")
async def request_otp(req: OTPRequest):
    """Generate OTP and send via Telegram to a registered user."""
    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.phone_number == req.phone_number))
        user = result.scalar_one_or_none()
        if not user or not user.telegram_id:
            raise HTTPException(
                status_code=404, detail="Phone number not registered with JanSevak Telegram Bot"
            )

        import random

        # Generate 4 digit OTP
        otp = str(random.randint(1000, 9999))

        # Save OTP in cache with 5 minute TTL (300 seconds)
        await query_cache.set_raw(f"otp:{req.phone_number}", otp, ttl=300)

        # Send OTP via Telegram
        bot = get_bot()
        message = f"🔐 Your JanSevak login OTP is: <b>{otp}</b>\n\nDo not share this with anyone."
        success = await send_notification(user.telegram_id, message, bot)
        await bot.session.close()

        if not success:
            raise HTTPException(status_code=500, detail="Failed to send OTP via Telegram")

        return {"status": "success", "message": "OTP sent successfully via Telegram"}


@router.post("/login")
async def login_citizen(req: CitizenLoginRequest):
    """Login a citizen with phone + OTP."""
    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.phone_number == req.phone_number))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify OTP
        cached_otp = await query_cache.get_raw(f"otp:{req.phone_number}")

        if not cached_otp:
            raise HTTPException(
                status_code=400, detail="OTP expired or not found. Please request a new one."
            )

        if cached_otp != req.otp:
            raise HTTPException(status_code=401, detail="Invalid OTP")

        # Delete OTP after successful use to prevent reuse
        if f"otp:{req.phone_number}" in query_cache._cache:
            del query_cache._cache[f"otp:{req.phone_number}"]

        # Generate proper JWT token
        expire = datetime.now(UTC) + timedelta(minutes=1440)  # 24 hours
        to_encode = {"sub": str(user.id), "type": "citizen", "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.admin_jwt_secret, algorithm="HS256")

        return {"access_token": encoded_jwt, "token_type": "bearer"}


@router.post("/dept/register")
async def register_dept_user(req: DeptRegisterRequest):
    """Register a new department user."""
    # Hash password securely
    password_hash = pwd_context.hash(req.password)

    async with async_session_factory() as session:
        result = await session.execute(
            select(DepartmentUser).where(DepartmentUser.email == req.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")

        dept_user = DepartmentUser(
            email=req.email,
            password_hash=password_hash,
            full_name=req.full_name,
            designation=req.designation,
            department_id=req.department_id,
            role="dept_viewer",
        )
        session.add(dept_user)
        await session.commit()
        return {"status": "success", "user_id": str(dept_user.id)}


@router.post("/dept/login")
async def login_dept_user(req: DeptLoginRequest):
    """Login a department user."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(DepartmentUser).where(DepartmentUser.email == req.email)
        )
        user = result.scalar_one_or_none()

        # Secure password check
        if not user or not pwd_context.verify(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate proper JWT token
        expire = datetime.now(UTC) + timedelta(minutes=1440)  # 24 hours
        to_encode = {"sub": str(user.id), "type": "dept", "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.admin_jwt_secret, algorithm="HS256")

        return {"access_token": encoded_jwt, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current logged in user."""
    try:
        payload = jwt.decode(token, settings.admin_jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    async with async_session_factory() as session:
        result = await session.execute(
            select(DepartmentUser).where(DepartmentUser.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

    return {"status": "success", "user": {"id": str(user.id), "email": user.email, "full_name": user.full_name}}
