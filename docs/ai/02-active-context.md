# JanSeva — Active Context

## Current Phase
**Phase 1: Deployment & Stabilization**

## Last Session (2026-07-03)
- Built the **Healthcare Agent** (Guide 09):
  - Created `HealthcareFacility` database model.
  - Built `healthcare_agent.py` to search facilities by district and simulate queue number generation.
  - Registered the healthcare intent in `orchestrator.py`.
  - Seeded sample data for Bhopal, Indore, and Delhi hospitals.

## Current Focus
Integrating the Healthcare Agent. Need to ensure the production database gets seeded with hospital data upon deployment.

## Next Steps
1. Push changes to Dokploy.
2. Build the Farmer Services Agent (Guide 10) or Admin Dashboard (Guide 07).

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
