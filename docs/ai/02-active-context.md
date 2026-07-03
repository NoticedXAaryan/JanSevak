# JanSeva — Active Context

## Current Phase
**Phase 1: Deployment & Stabilization**

## Last Session (2026-07-03)
- Built **Notifications & Interest Profiling** (Guide 11):
  - Created `profiler.py` using Gemini to extract interests and integrated into voice/text handlers as background tasks.
  - Added `notifications_enabled` to `User` DB model.
  - Built `engine.py` to broadcast scheme alerts to relevant users.
  - Created an asyncio `scheduler.py` loop (replacing ARQ/Redis) to periodically check for new alerts.
  - Added `/notifications on|off` command to the bot.

## Current Focus
Validating notifications functionality.

## Next Steps
1. Push changes to Dokploy.
2. Build WhatsApp Integration (Guide 12) or Scaling/Performance optimizations (Guide 13).

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
