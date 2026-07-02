# JanSeva — Active Context

## Current Phase
**Phase 0: Foundation & Documentation**

## Last Session (2026-07-02)
- Created project brief (`00-project-brief.md`)
- Created architecture document (`01-architecture.md`)
- Created active context (`02-active-context.md`)
- Creating implementation master guide (`03-implementation-master.md`)
- Creating all detailed implementation guides under `docs/ai/guides/`
- Research completed on: AI agent frameworks, Telegram bot frameworks, Hindi/Indian language voice tech, anonymous reporting platforms, databases, admin panels, task queues

## Current Focus
Building the complete documentation suite that serves as a self-contained implementation manual. No code has been written yet — documentation first, then implementation.

## Next Steps
1. Complete all implementation guide documents
2. Begin Phase 1 implementation: project scaffolding, database setup, basic Telegram bot
3. Build the AI agent layer (LangGraph orchestrator + specialist agents)
4. Build the anonymous reporting system
5. Integrate voice processing

## Key Decisions Made
- **Project name**: JanSeva (जनसेवा)
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
