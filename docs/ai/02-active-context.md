# JanSeva — Active Context

## Current Phase
**Phase 1: Deployment & Stabilization**

## Last Session (2026-07-03)
- Built **Scaling & Performance Optimizations** (Guide 13):
  - Tuned `engine.py` for increased DB connection pooling and recycling.
  - Added Alembic migration for critical DB indexes across users, conversations, messages, and reports.
  - Implemented an in-memory `AsyncTTLCache` to cache frequent identical AI queries (avoiding Redis dependency).
  - Added a `/health` endpoint to the FastAPI admin app.
  - Created a Locust load testing script.

## Current Focus
Validating performance optimizations under load.

## Next Steps
1. Push all changes to Dokploy.
2. Final end-to-end review of JanSeva platform!

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
