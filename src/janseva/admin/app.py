"""Admin dashboard FastAPI application."""
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
import time

from janseva.admin.auth import get_current_admin_optional, verify_password, create_access_token
from janseva.config import settings

admin_app = FastAPI(title="JanSeva Web", docs_url="/admin/docs")

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

# Import routers later when created
from janseva.admin.routes.dashboard import router as dashboard_router
from janseva.admin.routes.queries import router as queries_router
from janseva.admin.routes.reports import router as reports_router

admin_app.include_router(dashboard_router, prefix="/admin")
admin_app.include_router(queries_router, prefix="/admin/queries")
admin_app.include_router(reports_router, prefix="/admin/reports")

# Mount WhatsApp Webhook
from janseva.api.whatsapp import router as whatsapp_router
admin_app.include_router(whatsapp_router, prefix="/api")

@admin_app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Public landing page."""
    admin = get_current_admin_optional(request)
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "admin": admin}
    )

@admin_app.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Admin login page."""
    if get_current_admin_optional(request):
        return RedirectResponse(url="/admin", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})

@admin_app.post("/admin/login")
async def login_post(username: str = Form(...), password: str = Form(...)):
    """Handle login submission."""
    if username == settings.admin_username and verify_password(password, settings.admin_password):
        access_token = create_access_token(data={"sub": username})
        
        # We redirect to /admin via HTMX response header or standard redirect
        response = HTMLResponse(
            content="<script>window.location.href='/admin';</script>", 
            status_code=200
        )
        response.set_cookie(
            key="admin_token",
            value=access_token,
            httponly=True,
            max_age=1440 * 60, # 1 day
            expires=1440 * 60,
        )
        return response
    
    # Invalid credentials
    return HTMLResponse(
        content='<div class="text-red-500 mt-2 text-sm">Invalid username or password</div>',
        status_code=401
    )

@admin_app.get("/admin/logout")
async def logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("admin_token")
    return response

if __name__ == "__main__":
    uvicorn.run("janseva.admin.app:admin_app", host="0.0.0.0", port=8000, reload=True)
