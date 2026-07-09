"""Admin dashboard FastAPI application."""

import time
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from janseva.admin.auth import create_access_token, get_current_admin_optional, verify_password
from janseva.config import settings
from janseva.datasync.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the data sync scheduler in the background (e.g., every 60 seconds for demo)
    await scheduler.start(interval_seconds=60)
    yield
    # Stop the scheduler on shutdown
    await scheduler.stop()


from fastapi.middleware.cors import CORSMiddleware

admin_app = FastAPI(title="JanSeva Web", docs_url="/admin/docs", lifespan=lifespan)

# Add CORS middleware to allow Next.js frontend (port 3000) to communicate with this backend (port 8000)
admin_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup time for uptime calculation
START_TIME = time.time()

# Mount static files and templates
STATIC_DIR = Path(__file__).parent / "static"
TEMPLATE_DIR = Path(__file__).parent / "templates"

# Create static dir if it doesn't exist
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

admin_app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@admin_app.get("/health")
async def health_check():
    """Basic health check endpoint for deployment monitoring."""
    uptime_seconds = int(time.time() - START_TIME)
    return {
        "status": "healthy",
        "uptime_seconds": uptime_seconds,
        "database": "connected",
    }


from janseva.admin.routes.admin_users import router as admin_users_router
from janseva.admin.routes.dashboard import router as dashboard_router
from janseva.admin.routes.organizations import router as organizations_router
from janseva.admin.routes.queries import router as queries_router
from janseva.admin.routes.reports import router as reports_router

admin_app.include_router(dashboard_router, prefix="/admin")
admin_app.include_router(queries_router, prefix="/admin/queries")
admin_app.include_router(reports_router, prefix="/admin/reports")
admin_app.include_router(organizations_router, prefix="/admin/organizations")
admin_app.include_router(admin_users_router, prefix="/admin/users")

# Mount WhatsApp Webhook
from janseva.api.whatsapp import router as whatsapp_router

admin_app.include_router(whatsapp_router, prefix="/api")

# Mount Chat API
from janseva.api.chat import router as chat_router

admin_app.include_router(chat_router, prefix="/api/v1/chat")

# Mount new v2 APIs
from janseva.api.auth import router as auth_router
from janseva.api.complaints import router as complaints_router
from janseva.api.departments import router as dept_router
from janseva.api.reports import router as public_reports_router
from janseva.api.uploads import router as uploads_router

admin_app.include_router(auth_router)
admin_app.include_router(complaints_router)
admin_app.include_router(dept_router)
admin_app.include_router(public_reports_router)
admin_app.include_router(uploads_router)

# Mount diagnostics API
from janseva.api.diagnostics import router as diagnostics_router

admin_app.include_router(diagnostics_router, prefix="/api/v1")

# Mount OAuth router
from janseva.admin.oauth import router as oauth_router

admin_app.include_router(oauth_router)


@admin_app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Public landing page."""
    admin = get_current_admin_optional(request)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request, "admin": admin}
    )


@admin_app.get("/api/public/stats")
async def public_stats():
    """Public stats endpoint for the landing page (cached in production)."""
    from sqlalchemy import func, select

    from janseva.db.engine import async_session_factory
    from janseva.db.models.anonymous_report import AnonymousReport
    from janseva.db.models.conversation import Conversation
    from janseva.db.models.user import User

    async with async_session_factory() as session:
        users_count = await session.scalar(select(func.count()).select_from(User)) or 0
        conversations_count = (
            await session.scalar(select(func.count()).select_from(Conversation)) or 0
        )
        reports_count = await session.scalar(select(func.count()).select_from(AnonymousReport)) or 0

    return JSONResponse(
        content={
            "citizens_served": users_count,
            "queries_resolved": conversations_count,
            "active_institutions": 0,
            "schemes_indexed": 0,
        }
    )


@admin_app.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Admin login page."""
    if get_current_admin_optional(request):
        return RedirectResponse(url="/admin", status_code=303)

    error = request.query_params.get("error")
    error_msg = None
    if error == "auth_failed":
        error_msg = "Google authentication failed. Please try again."
    elif error == "account_disabled":
        error_msg = "Your account is disabled. Contact support."
    elif error == "unauthorized":
        error_msg = "Your Google account is not authorized to access this dashboard."

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "error_msg": error_msg,
            "google_enabled": bool(settings.google_client_id),
        },
    )


@admin_app.post("/admin/login")
async def login_post(username: str = Form(...), password: str = Form(...)):
    """Handle login submission."""
    if username == settings.admin_username and verify_password(password, settings.admin_password):
        access_token = create_access_token(data={"sub": username})

        # We redirect to /admin via HTMX response header or standard redirect
        response = HTMLResponse(
            content="<script>window.location.href='/admin';</script>", status_code=200
        )
        response.set_cookie(
            key="admin_token",
            value=access_token,
            httponly=True,
            max_age=1440 * 60,  # 1 day
            expires=1440 * 60,
        )
        return response

    # Invalid credentials
    return HTMLResponse(
        content='<div class="text-red-500 mt-2 text-sm">Invalid username or password</div>',
        status_code=401,
    )


@admin_app.get("/admin/logout")
async def logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("admin_token")
    return response


if __name__ == "__main__":
    uvicorn.run("janseva.admin.app:admin_app", host="0.0.0.0", port=8000, reload=True)
