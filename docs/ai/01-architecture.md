# JanSeva — Architecture & Technology Stack

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MESSAGING LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Telegram Bot  │  │ WhatsApp Bot │  │ Future Channels          │  │
│  │ (aiogram 3.x) │  │ (Phase 2)    │  │ (Web Widget, USSD, etc.) │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────────┘  │
│         │                  │                      │                  │
│         └──────────────────┴──────────────────────┘                  │
│                            │                                         │
│                    ┌───────▼───────┐                                 │
│                    │ Channel Router │  (Normalizes input from any    │
│                    │ & Normalizer   │   channel into unified format) │
│                    └───────┬───────┘                                 │
└────────────────────────────┼────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                        VOICE LAYER                                  │
│  ┌─────────────────────┐      ┌─────────────────────┐              │
│  │ Speech-to-Text (STT) │      │ Text-to-Speech (TTS) │             │
│  │ AI4Bharat IndicASR   │      │ AI4Bharat IndicTTS   │             │
│  │ or IndicWhisper      │      │                      │             │
│  └──────────┬──────────┘      └──────────▲──────────┘              │
│             │                             │                         │
└─────────────┼─────────────────────────────┼─────────────────────────┘
              │                             │
┌─────────────▼─────────────────────────────┼─────────────────────────┐
│                      AI AGENT LAYER (LangGraph)                      │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Orchestrator Agent                         │    │
│  │  (Intent Classification → Route to Specialist Agent)         │    │
│  └──┬──────────┬──────────┬──────────┬──────────┬──────────┬───┘    │
│     │          │          │          │          │          │          │
│  ┌──▼──┐  ┌───▼──┐  ┌───▼──┐  ┌───▼──┐  ┌───▼──┐  ┌───▼──┐      │
│  │Svc  │  │Anon  │  │Health│  │Farm  │  │Notif │  │Escal │      │
│  │Nav  │  │Report│  │Care  │  │Svc   │  │Agent │  │Agent │      │
│  │Agent│  │Agent │  │Agent │  │Agent │  │      │  │      │      │
│  └──┬──┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘      │
│     │        │         │         │          │         │            │
│  ┌──▼────────▼─────────▼─────────▼──────────▼─────────▼──┐        │
│  │               Tool Registry                            │        │
│  │  (DB queries, form generation, geo-lookup, etc.)       │        │
│  └────────────────────────┬───────────────────────────────┘        │
└───────────────────────────┼────────────────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────────────────┐
│                      DATA & STORAGE LAYER                          │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ PostgreSQL    │  │ Redis        │  │ Vector Store             │ │
│  │ (Primary DB)  │  │ (Cache,Queue,│  │ (ChromaDB / pgvector)   │ │
│  │               │  │  Sessions)   │  │ (RAG Knowledge Base)    │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────────────────┐
│                      ADMIN & MONITORING                            │
│                                                                    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │ Admin Dashboard   │  │ Monitoring &     │  │ Report Routing  │ │
│  │ (FastAPI + HTMX)  │  │ Logging          │  │ Engine          │ │
│  │                   │  │ (Structured JSON) │  │                 │ │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## Technology Stack — Detailed Choices

### 1. Messaging Interface

| Component | Technology | Why |
|-----------|-----------|-----|
| **Telegram Bot** | `aiogram 3.x` | Async-native, modern router architecture, built for high-concurrency bots. Preferred over `python-telegram-bot` for performance-oriented apps |
| **WhatsApp Bot** (Phase 2) | Twilio WhatsApp API or WhatsApp Business Cloud API | Official, reliable, supports media messages |
| **Channel Normalizer** | Custom Python module | Translates platform-specific message formats into a unified internal schema |

### 2. AI Agent Framework

| Component | Technology | Why |
|-----------|-----------|-----|
| **Agent Orchestration** | `LangGraph` (by LangChain) | Production-grade stateful workflows as directed graphs. Supports checkpointing, human-in-the-loop, and complex branching. Industry standard for 2025-2026 |
| **LLM Provider** | Google Gemini API (primary), Ollama + Llama 3 (fallback/dev) | Gemini for production quality; Ollama for local development without API costs |
| **RAG / Knowledge Base** | `LangChain` + `ChromaDB` (or `pgvector`) | Retrieval-Augmented Generation for querying government service knowledge base |
| **Prompt Management** | LangChain PromptTemplates + custom YAML configs | Separates prompt engineering from code logic |

### 3. Voice Processing

| Component | Technology | Why |
|-----------|-----------|-----|
| **Speech-to-Text** | AI4Bharat `IndicWhisper` (fine-tuned OpenAI Whisper for Indian languages) | Best open-source STT for Hindi + 21 other scheduled Indian languages. Handles code-mixing (Hinglish) |
| **Text-to-Speech** | AI4Bharat `IndicTTS` | Matched pair to IndicWhisper — same language coverage, natural-sounding voices |
| **Language Detection** | `langdetect` or Whisper's built-in detection | Auto-detect user's language from voice input to respond in same language |
| **Audio Processing** | `pydub` + `ffmpeg` | Convert Telegram's OGG voice notes to WAV for model input |

### 4. Database & Storage

| Component | Technology | Why |
|-----------|-----------|-----|
| **Primary Database** | PostgreSQL 16+ | Production-grade, MVCC concurrency, JSONB for flexible data, pgvector extension for embeddings, strong audit/compliance features |
| **ORM** | SQLAlchemy 2.x (async) | Industry standard, type-safe, migration support via Alembic |
| **Migrations** | Alembic | Forward-only, reviewed, reversible migrations |
| **Cache / Session Store** | Redis 7.x | Conversation state caching, rate limiting, task queue broker |
| **Vector Store** | ChromaDB (dev) → pgvector (prod) | ChromaDB for fast iteration; pgvector in production to avoid another running service |
| **File Storage** | Local filesystem (dev) → S3-compatible (prod) | Generated forms, voice recordings (anonymized) |

### 5. Backend API

| Component | Technology | Why |
|-----------|-----------|-----|
| **Web Framework** | FastAPI | Async-native, auto-docs (OpenAPI), Pydantic validation, high performance |
| **Task Queue** | ARQ (Redis-backed, async-native) | Lightweight, async-first — better fit than Celery for our async FastAPI stack |
| **Admin Panel** | Custom FastAPI + HTMX + Jinja2 | Lightweight, server-rendered admin dashboard. No SPA overhead |
| **Auth (Admin)** | FastAPI + JWT + bcrypt | Simple, proven auth for the admin panel |

### 6. Infrastructure & DevOps

| Component | Technology | Why |
|-----------|-----------|-----|
| **Containerization** | Docker + Docker Compose | Environment parity, reproducible builds |
| **Process Manager** | Docker Compose (dev), systemd (single-server prod) | Simple orchestration without Kubernetes overhead at this scale |
| **Logging** | `structlog` (structured JSON logging) | Machine-parseable logs for debugging and monitoring |
| **Monitoring** | Health check endpoints + Prometheus metrics (optional Phase 2) | Basic health checks first, full observability later |
| **Reverse Proxy** | Caddy or Nginx | TLS termination, webhook routing. Caddy for auto-HTTPS simplicity |

### 7. Development Tools

| Component | Technology | Why |
|-----------|-----------|-----|
| **Package Manager** | `uv` | 10-100x faster than pip, lockfile support, replaces pip + pip-tools + virtualenv |
| **Linting** | `ruff` | Fast, replaces flake8 + isort + pyupgrade in one tool |
| **Type Checking** | `mypy` (strict mode) | Catch type errors before runtime |
| **Testing** | `pytest` + `pytest-asyncio` | Standard Python testing with async support |
| **Pre-commit** | `pre-commit` hooks | Enforce formatting/linting before every commit |

---

## Key Design Decisions (ADRs)

### ADR-001: aiogram over python-telegram-bot
**Decision**: Use `aiogram 3.x` for the Telegram bot layer.
**Why**: aiogram is built on pure asyncio, has a modern router/dispatcher architecture that avoids spaghetti code as we add more handlers, and handles high concurrency better. python-telegram-bot is more beginner-friendly but aiogram is better for a production system that needs to handle 100+ concurrent users.

### ADR-002: LangGraph over CrewAI/AutoGen
**Decision**: Use LangGraph for agent orchestration.
**Why**: LangGraph provides explicit state machines (vs. CrewAI's role-based delegation or AutoGen's conversational patterns). Government services have deterministic workflows that benefit from explicit graph-based control flow. LangGraph's checkpointing also gives us fault tolerance — if the bot crashes mid-conversation, users can resume where they left off.

### ADR-003: AI4Bharat IndicWhisper for Voice
**Decision**: Use AI4Bharat's IndicWhisper for speech-to-text.
**Why**: Purpose-built for Indian languages. Handles code-mixing (Hindi + English in same sentence), supports all 22 scheduled languages, and is open-source. Generic Whisper struggles with Indian accents and regional languages. IndicWhisper models are available on HuggingFace.

### ADR-004: PostgreSQL + pgvector over separate vector DB
**Decision**: Start with ChromaDB for development, migrate to pgvector for production.
**Why**: One less service to manage in production. pgvector lives inside PostgreSQL, so we get relational + vector search in one database. ChromaDB is faster to iterate with during development.

### ADR-005: ARQ over Celery for Task Queue
**Decision**: Use ARQ instead of Celery.
**Why**: ARQ is async-native (no worker pool hacks needed with FastAPI), simpler configuration, Redis-backed (which we already use for caching). Celery is overkill for our scale and doesn't play well with asyncio without workarounds.

### ADR-006: Anonymous Reporting — Security Architecture
**Decision**: Reports are encrypted at rest, stripped of metadata, and stored with no link to the sender's Telegram ID.
**Why**: The anonymous reporting feature is high-stakes. If a report about a local police inspector can be traced back to the reporter, it could endanger them. The system generates a one-time anonymous report ID for two-way communication. The report routing engine automatically identifies the correct superior authority based on a hierarchy map, bypassing any named official in the complaint.

---

## Data Model Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   users      │     │ conversations│     │ messages         │
│─────────────│     │──────────────│     │─────────────────│
│ id (UUID)    │──┐  │ id (UUID)    │──┐  │ id (UUID)        │
│ telegram_id  │  └─>│ user_id (FK) │  └─>│ conversation_id  │
│ language     │     │ agent_type   │     │ role (user/ai)   │
│ district     │     │ state (JSON) │     │ content          │
│ interests[]  │     │ status       │     │ voice_audio_ref  │
│ created_at   │     │ created_at   │     │ language         │
│ updated_at   │     │ updated_at   │     │ created_at       │
└─────────────┘     └──────────────┘     └─────────────────┘

┌──────────────────┐     ┌──────────────────┐
│ anonymous_reports │     │ service_catalog   │
│──────────────────│     │──────────────────│
│ id (UUID)         │     │ id (UUID)         │
│ report_token      │     │ name_en           │
│ category          │     │ name_hi           │
│ content_encrypted │     │ department        │
│ target_authority  │     │ requirements[]    │
│ authority_level   │     │ forms[]           │
│ status            │     │ district_specific │
│ admin_notes       │     │ created_at        │
│ routed_to_dept    │     │ updated_at        │
│ created_at        │     └──────────────────┘
│ resolved_at       │
└──────────────────┘     ┌──────────────────┐
                         │ escalated_queries │
┌──────────────────┐     │──────────────────│
│ authority_hierarchy│    │ id (UUID)         │
│──────────────────│     │ user_id (FK)      │
│ id (UUID)         │     │ original_query    │
│ title             │     │ category          │
│ department        │     │ department        │
│ district          │     │ status            │
│ level (int)       │     │ admin_response    │
│ reports_to (FK)   │     │ assigned_to       │
│ contact_info_enc  │     │ created_at        │
└──────────────────┘     │ resolved_at       │
                         └──────────────────┘
```

---

## Known Technical Debt & Risks

1. **Voice model hosting**: IndicWhisper models are large (~1.5GB+). Need GPU or at minimum a powerful CPU for real-time transcription. May need to use Bhashini API as a cloud alternative if self-hosting is not feasible.
2. **Knowledge base cold start**: The RAG system needs to be populated with actual government service data. This is a data collection effort, not a code problem.
3. **Authority hierarchy data**: The anonymous reporting routing engine requires a maintained database of government authority hierarchies per district. This data doesn't exist in a structured format and needs to be manually compiled.
4. **Rate limiting**: Telegram API has rate limits (30 messages/second per bot, 20 messages/minute per chat). The system must respect these.
