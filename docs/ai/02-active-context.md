# JanSeva — Active Context

## Current Phase
**Phase 1: Deployment & Stabilization**

## Last Session (2026-07-03)
- Built **WhatsApp Integration** (Guide 12):
  - Added Twilio credentials to configuration.
  - Implemented `twilio_client.py` for sending async REST requests to Twilio.
  - Created a FastAPI webhook router (`whatsapp.py`) to handle incoming Twilio requests.
  - Applied the Channel Normalizer pattern by parsing WhatsApp numbers into pseudo-telegram IDs and passing them into the existing AI agent pipeline.

## Current Focus
Validating WhatsApp webhook functionality.

## Next Steps
1. Push changes to Dokploy.
2. Build Scaling/Performance optimizations (Guide 13).

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
