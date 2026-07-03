# JanSeva — Active Context

## Current Phase
**Phase 1: Deployment & Stabilization**

## Last Session (2026-07-03)
- Built the **Voice Processing Pipeline** (Guide 08):
  - Added `openai-whisper` and `pydub` dependencies.
  - Implemented STT (`stt.py`) and audio conversions (`audio_utils.py`).
  - Integrated full Voice-to-Text routing into the Telegram `voice.py` router so users can send voice notes and get text responses.

## Current Focus
Integrating the Voice Processing Pipeline. Ensure the deployment container has `ffmpeg` installed for `pydub` to function correctly.

## Next Steps
1. Push changes to Dokploy.
2. Build the remaining agents (Healthcare, Farmer) or Admin Dashboard (Guide 07).

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
