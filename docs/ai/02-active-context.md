# JanSevak — Active Context

## Current Phase
**Phase: V2 Redesign — Multi-Institution Platform**

## Last Session (2026-07-04)
- Conducted full codebase audit of web frontend, backend, models, agents, knowledge base
- Identified that the Next.js frontend is a single page (landing only) — no routing, no dashboards, no chatbot UI
- Researched 20 Indian government institution types across 8 sectors
- Created comprehensive implementation plan for v2: 45+ pages, 20 institution dashboards, AI chatbot UI, citizen portal
- Plan awaiting user review and approval before execution

## Current Focus
🏗️ **V2 MULTI-INSTITUTION REBUILD** — Transforming JanSevak from a single landing page into a complete government services platform with:
- 20 tailored institution dashboards (healthcare, police, education, revenue, civic, welfare, agriculture, representatives)
- Full citizen portal (services directory, schemes explorer, institution finder, grievance tracker)
- Web-based AI chatbot (not just Telegram wrapper)
- Role-based auth for citizens, institution admins, and elected representatives
- Complete public-facing website (about, contact, FAQ, privacy, terms, accessibility)

## Key Decisions Pending
- Auth strategy: Phone+OTP vs Email+Password vs both
- Data: Real vs demo data for dashboards
- Chat transport: WebSocket vs SSE
- Dashboard depth: Mock data breadth vs real forms depth
- Execution priority ordering

## What Already Exists (Backend — Reusable)
- FastAPI admin with JWT auth, Google OAuth
- Organization model with multi-type support
- AdminUser model with roles (super_admin, org_admin, org_viewer)
- AI agents: Orchestrator, ServiceNavigator, HealthcareAgent, FarmerAgent, AnonymousReporter, Escalation
- Knowledge base with YAML data for schemes, services, subsidies, healthcare
- Telegram bot with LangGraph integration
- PostgreSQL + ChromaDB data layer

## What Needs to Be Built (Frontend)
- 45+ Next.js pages (currently: 1)
- 22+ reusable components (currently: 1)
- 3 layout shells (public, dashboard, auth)
- Design system overhaul
- API client layer
- Chat UI with streaming
- Dashboard with charts, tables, forms, maps
