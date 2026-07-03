# JanSeva — Active Context

## Current Phase
**Phase 1: Deployment & Stabilization**

## Last Session (2026-07-03)
- Built the **Anonymous Reporting System** (Guide 05):
  - Created `Authority` and `AnonymousReport` database models with no user FK to guarantee anonymity.
  - Implemented AES-128-CBC (Fernet) encryption for report contents at rest.
  - Implemented metadata stripping (phone numbers, Aadhaar, email, Telegram usernames).
  - Built smart routing to automatically route complaints to a superior if a specific official is named.
  - Built the `anonymous_reporter` LangGraph conversational node and integrated it into the central orchestrator.

## Current Focus
Integrating the newly built Anonymous Reporting System into production and verifying that reports are successfully encrypted and routed.

## Next Steps
1. Push changes to Dokploy and supply the `REPORT_ENCRYPTION_KEY` environment variable.
2. Integrate voice processing (Guide 06).

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
