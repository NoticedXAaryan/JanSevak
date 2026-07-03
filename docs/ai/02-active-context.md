# JanSeva — Active Context

## Current Phase
**Phase 1: Deployment & Stabilization**

## Last Session (2026-07-03)
- Built the **Admin Dashboard** (Guide 07):
  - Created a FastAPI sub-app with JWT cookie auth.
  - Built a public landing page (`index.html`) linking to Telegram.
  - Implemented HTMX-powered dashboard routes for viewing stats, user queries, and managing anonymous reports.
  - Updated `start.sh` to spin up the web server alongside the Telegram bot.

## Current Focus
Integrating the Admin Dashboard. The web server now runs on port 8000 alongside the bot.

## Next Steps
1. Push changes to Dokploy.
2. Build Profile Notifications (Guide 11) or WhatsApp Integration (Guide 12).

## Key Decisions Made
- **Deployment Architecture**: Bot-only container with an external Managed PostgreSQL database. No local Redis or Postgres containers to preserve VPS disk space.
- **Telegram framework**: aiogram 3.x (async-native, modern architecture)
- **Agent framework**: LangGraph (stateful workflows, checkpointing, explicit control flow)
- **Voice STT**: AI4Bharat IndicWhisper (best open-source for Indian languages)
- **Database**: PostgreSQL + pgvector (single service for relational + vector data)
- **Task queue**: ARQ (async-native, simpler than Celery for our stack)
- **Admin panel**: Custom FastAPI + HTMX (lightweight, no SPA overhead)

## Open Questions
- Which specific districts/states to target for initial knowledge base data?
- Self-host voice models or use Bhashini API for transcription?
- LLM provider: Gemini API key availability and budget for production?
