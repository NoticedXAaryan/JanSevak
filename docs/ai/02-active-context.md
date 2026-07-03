# JanSeva — Active Context

## Current Phase
**Phase 1: Deployment & Stabilization**

## Last Session (2026-07-03)
- Resolved critical `ModuleNotFoundError` during Dokploy deployment:
  - Root cause was an unanchored `models/` rule in `.gitignore` that excluded the `src/janseva/db/models` directory from GitHub.
  - Fixed by anchoring to `/models/` and committing the database models.
- Resolved `uv sync` failure during container runtime:
  - `uv run` inside the container forced a re-sync and wiped the installation.
  - Fixed by calling `.venv/bin/python` directly in `scripts/start.sh`.
- Removed local `postgres` and `redis` from `docker-compose.yml`:
  - Adopted external managed PostgreSQL to save local disk space on the VPS.
  - Redis was dropped as rate-limiting currently uses in-memory logic.

## Current Focus
Monitoring the stability of the Dokploy deployment and confirming the external PostgreSQL instance connection is functioning properly with URL-encoded passwords.

## Next Steps
1. Finalize the deployment using the external DB.
2. Build the AI agent layer (LangGraph orchestrator + specialist agents).
3. Build the anonymous reporting system.
4. Integrate voice processing.

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
