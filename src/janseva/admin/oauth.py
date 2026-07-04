"""
Google OAuth integration using Authlib.
"""
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
import sqlalchemy
from sqlalchemy import select
import structlog
from datetime import datetime, timezone

from janseva.config import settings
from janseva.db.engine import async_session_factory
from janseva.db.models.admin_user import AdminUser
from janseva.admin.auth import create_access_token

logger = structlog.get_logger()

# Set up OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

router = APIRouter(prefix="/admin/auth/google", tags=["admin-auth"])

@router.get("/login")
async def google_login(request: Request):
    """Redirects to Google for authentication."""
    redirect_uri = settings.google_redirect_uri
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def google_callback(request: Request):
    """Handles callback from Google, issues JWT, and redirects to dashboard."""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if not user_info:
            logger.error("google_auth_failed_no_userinfo")
            return RedirectResponse(url='/admin/login?error=auth_failed')
            
        email = user_info.get('email')
        name = user_info.get('name')
        picture = user_info.get('picture')
        
        async with async_session_factory() as session:
            # Check if user exists
            result = await session.execute(select(AdminUser).where(AdminUser.email == email))
            admin_user = result.scalar_one_or_none()
            
            if admin_user:
                if not admin_user.is_active:
                    logger.warning("inactive_admin_attempted_login", email=email)
                    return RedirectResponse(url='/admin/login?error=account_disabled')
                    
                # Update existing user
                admin_user.full_name = name
                if picture:
                    admin_user.avatar_url = picture
                admin_user.last_login = datetime.now(timezone.utc)
            else:
                # For safety, we only auto-provision if it's the first user ever, 
                # OR we don't auto-provision and require a super_admin to create them first.
                # Let's see if this is the very first admin.
                count = await session.scalar(select(sqlalchemy.func.count()).select_from(AdminUser))
                if count == 0:
                    # First user becomes super_admin
                    admin_user = AdminUser(
                        email=email,
                        full_name=name,
                        avatar_url=picture,
                        role="super_admin"
                    )
                    session.add(admin_user)
                else:
                    # Reject unauthorized logins
                    logger.warning("unauthorized_admin_login_attempt", email=email)
                    return RedirectResponse(url='/admin/login?error=unauthorized')
                    
            await session.commit()
            
            # Create JWT
            access_token = create_access_token(data={
                "sub": email,
                "role": admin_user.role,
                "org_id": str(admin_user.organization_id) if admin_user.organization_id else None
            })
            
            response = RedirectResponse(url="/admin", status_code=303)
            response.set_cookie(
                key="admin_token",
                value=access_token,
                httponly=True,
                max_age=1440 * 60, # 1 day
                expires=1440 * 60,
            )
            return response
            
    except Exception as e:
        logger.error("google_auth_exception", error=str(e))
        return RedirectResponse(url='/admin/login?error=auth_failed')
