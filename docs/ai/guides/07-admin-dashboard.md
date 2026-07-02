# Guide 07: Admin Dashboard

## What This Does
Builds a lightweight web dashboard for administrators to manage JanSeva. The admin panel is a server-rendered FastAPI app using HTMX for interactivity — no heavy SPA framework needed.

## Prerequisites
- Guide 01 completed (project setup)
- Guide 05 completed (anonymous reports exist in DB)
- Guide 06 completed (escalated queries exist in DB)

---

## Features

### Pages

1. **Login** — JWT-based admin authentication
2. **Dashboard Home** — Overview stats: total users, queries today, pending escalations, open reports
3. **Escalated Queries** — View, assign, respond to queries AI couldn't answer
4. **Anonymous Reports** — View anonymized reports, add admin notes, update status
5. **Knowledge Base Manager** — Add/edit/delete service catalog YAML entries (triggers re-ingestion)
6. **User Analytics** — Usage trends, popular queries, language distribution

### Tech Stack
- **Backend**: FastAPI (separate app from the bot, same codebase)
- **Templating**: Jinja2 (server-rendered HTML)
- **Interactivity**: HTMX (dynamic updates without full page reloads)
- **Styling**: Minimal CSS (dark theme, monochrome, professional)
- **Auth**: JWT tokens stored in httpOnly cookies

---

## Implementation Steps

### 1. Create the Admin FastAPI App

**File: `src/janseva/admin/app.py`**

```python
"""Admin dashboard FastAPI application."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

admin_app = FastAPI(title="JanSeva Admin", docs_url="/admin/docs")

# Mount static files and templates
STATIC_DIR = Path(__file__).parent / "static"
TEMPLATE_DIR = Path(__file__).parent / "templates"

admin_app.mount("/admin/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# Import and register routes
from janseva.admin.routes.dashboard import router as dashboard_router
from janseva.admin.routes.queries import router as queries_router
from janseva.admin.routes.reports import router as reports_router

admin_app.include_router(dashboard_router, prefix="/admin")
admin_app.include_router(queries_router, prefix="/admin/queries")
admin_app.include_router(reports_router, prefix="/admin/reports")
```

### 2. Authentication

- Admin credentials from `.env` (ADMIN_USERNAME, ADMIN_PASSWORD)
- On login: verify credentials → issue JWT → set as httpOnly cookie
- Middleware checks JWT on every admin route
- Password hashed with bcrypt

### 3. Dashboard Routes

Each route renders a Jinja2 template. HTMX handles:
- Loading escalated queries list without full page reload
- Submitting admin responses inline
- Updating report status via dropdown

### 4. Running the Admin Panel

```bash
# Run alongside the bot (separate process):
uv run uvicorn janseva.admin.app:admin_app --host 0.0.0.0 --port 8000 --reload
```

Then visit `http://localhost:8000/admin/`

---

## Key Templates to Create

- `templates/base.html` — Layout with nav, dark theme CSS
- `templates/login.html` — Login form
- `templates/dashboard.html` — Stats overview
- `templates/queries.html` — Escalated queries table with response forms
- `templates/reports.html` — Anonymous reports with status management

---

## Git Checkpoint

```bash
git add -A
git commit -m "feat(admin): implement admin dashboard with HTMX

- FastAPI admin app with JWT cookie auth
- Dashboard overview with stats
- Escalated queries management (view, assign, respond)
- Anonymous reports viewer (status updates, admin notes)
- Dark theme, server-rendered with HTMX interactivity"
```
