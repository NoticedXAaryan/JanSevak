"""Authentication API for JanSevak v2."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
import uuid

from janseva.db.engine import async_session_factory
from janseva.db.models.user import User
from janseva.db.models.department_user import DepartmentUser

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# --- Schemas ---
class CitizenRegisterRequest(BaseModel):
    phone_number: str
    full_name: str
    pin_code: str | None = None
    state: str | None = None
    district: str | None = None

class CitizenLoginRequest(BaseModel):
    phone_number: str
    otp: str  # For demo purposes, any 4 digit OTP works

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
            district=req.district
        )
        session.add(user)
        await session.commit()
        return {"status": "success", "user_id": str(user.id)}

@router.post("/login")
async def login_citizen(req: CitizenLoginRequest):
    """Login a citizen with phone + OTP."""
    # In a real app, verify OTP here. For hackathon, accept anything.
    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.phone_number == req.phone_number))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Return a mock JWT token
        return {"access_token": f"mock_token_{user.id}", "token_type": "bearer"}

@router.post("/dept/register")
async def register_dept_user(req: DeptRegisterRequest):
    """Register a new department user."""
    # Hash password in real app
    password_hash = f"hashed_{req.password}"
    
    async with async_session_factory() as session:
        result = await session.execute(select(DepartmentUser).where(DepartmentUser.email == req.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
            
        dept_user = DepartmentUser(
            email=req.email,
            password_hash=password_hash,
            full_name=req.full_name,
            designation=req.designation,
            department_id=req.department_id,
            role="dept_viewer"
        )
        session.add(dept_user)
        await session.commit()
        return {"status": "success", "user_id": str(dept_user.id)}

@router.post("/dept/login")
async def login_dept_user(req: DeptLoginRequest):
    """Login a department user."""
    async with async_session_factory() as session:
        result = await session.execute(select(DepartmentUser).where(DepartmentUser.email == req.email))
        user = result.scalar_one_or_none()
        
        # Simple mock password check
        if not user or user.password_hash != f"hashed_{req.password}":
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        return {"access_token": f"mock_dept_token_{user.id}", "token_type": "bearer"}

@router.get("/me")
async def get_current_user():
    """Get current logged in user (mock)."""
    # Requires proper JWT dependency injection
    return {"status": "not_implemented"}
