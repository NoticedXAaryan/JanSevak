# 🙏 JanSeva (जनसेवा) — AI-Powered Government Services Platform

> **"Service to the People"** — Simplifying citizen interactions with Indian government authorities through AI, starting on Telegram.

---

## What is JanSeva?

JanSeva is an AI-powered conversational platform that helps Indian citizens navigate government bureaucracy. Instead of traveling to government offices, standing in queues, and filling confusing forms, citizens can simply send a message (text or voice) in Hindi or any Indian language and get:

- 📋 **Service Requirements** — "What do I need for an income certificate?"
- 📝 **Form Generation** — Pre-filled application forms
- 🚨 **Anonymous Reporting** — Safely report corruption or misconduct
- 🏥 **Healthcare Help** — Find hospitals, book appointments
- 🌾 **Farmer Services** — Navigate subsidies, check mandi prices
- 🔔 **Smart Notifications** — Get alerted about relevant schemes and deadlines

## Architecture

```
Telegram / WhatsApp → Channel Normalizer → LangGraph AI Agents → Response
                                                    ↕
                              PostgreSQL + Redis + ChromaDB (Knowledge Base)
                                                    ↕
                                        Admin Dashboard (FastAPI + HTMX)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Messaging** | aiogram 3.x (Telegram), WhatsApp Business API |
| **AI Agents** | LangGraph + LangChain |
| **LLM** | Google Gemini / Ollama (local) |
| **Voice** | AI4Bharat IndicWhisper (STT) + IndicTTS |
| **Database** | PostgreSQL 16 + Redis 7 |
| **Vector Store** | ChromaDB (dev) → pgvector (prod) |
| **Backend** | FastAPI + Pydantic |
| **Admin** | FastAPI + HTMX + Jinja2 |
| **Task Queue** | ARQ (async, Redis-backed) |
| **Infra** | Docker Compose |

## Design Philosophy & Compliance

JanSeva uses a split frontend architecture to meet the specific needs of citizens vs government officials:

### 1. Public Facing Landing Page (Next.js)
The public marketing site (`web/`) is built in Next.js to provide a highly interactive, modern, and trustworthy first impression for citizens discovering the project. It showcases live stats and the platform's capabilities visually.

### 2. Internal Admin Dashboard (Jinja2 + HTMX)
The actual operational dashboard (`src/janseva/admin/`) strictly adheres to Indian government cybersecurity and accessibility guidelines for internal tools. This air-gapped ready architecture is an intentional, compliance-driven choice:

- **Zero Third-Party Phone-Homes:** Government platforms operate on isolated internal networks. We do not rely on external CDNs (all assets like HTMX and fonts are bundled locally).
- **Maximum Accessibility & Low Bandwidth:** Rural officials often operate on older devices with 2G/3G connections. SSR HTML guarantees an extremely small initial payload.
- **Progressive Interactivity:** HTMX provides SPA-like capabilities (dynamic updates, modals) without the complexity of a Node.js runtime on the protected internal server.
- **Decade-Long Maintainability:** "Boring" and proven technologies like HTML, CSS, and Jinja2 are highly stable. Future government contractors can easily maintain this codebase 10 years from now.

## Quick Start

### Docker / Dokploy

```bash
# 1. Copy and configure environment
cp .env.example .env
# Fill TELEGRAM_BOT_TOKEN and GOOGLE_API_KEY.
# Compose derives container-safe DATABASE_URL/REDIS_URL values from
# POSTGRES_* and REDIS_HOST, so it will not use localhost by accident.

# 2. Build and start the full stack
docker compose up -d --build

# 3. View logs
docker compose logs -f bot
```

For a CPU-only VPS, use cloud LLM/embedding APIs and do not add PyTorch, Whisper, CUDA, or local model dependencies to the default Docker image. See [Deployment](docs/deployment.md) for the Dokploy checklist.

### Local Development

```bash
# 1. Clone and enter the project
cd GoogleXParul

# 2. Install dependencies
uv sync

# 3. Copy and configure environment
cp .env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN and GOOGLE_API_KEY
# If running the bot directly on your host, change postgres/redis hostnames
# in DATABASE_URL, DATABASE_URL_SYNC, and REDIS_URL to localhost.

# 4. Start database services
docker compose up -d

# 5. Run database migrations
uv run alembic upgrade head

# 6. Seed the knowledge base
uv run python scripts/seed_knowledge_base.py

# 7. Start the bot
uv run python -m janseva.bot.main
```

## Documentation

All documentation lives in `docs/ai/`:

| Document | Description |
|----------|-------------|
| [Project Brief](docs/ai/00-project-brief.md) | Vision, scope, and success metrics |
| [Architecture](docs/ai/01-architecture.md) | Tech stack, data model, design decisions |
| [Active Context](docs/ai/02-active-context.md) | Current state and next steps |
| [Master Guide](docs/ai/03-implementation-master.md) | **Start here** — Complete implementation roadmap |
| [Deployment](docs/deployment.md) | CPU-only VPS and Dokploy deployment checklist |

### Implementation Guides (in order)

| # | Guide | Phase | Status |
|---|-------|-------|--------|
| 01 | [Project Setup](docs/ai/guides/01-project-setup.md) | Foundation | 📝 Ready |
| 02 | [Telegram Bot](docs/ai/guides/02-telegram-bot.md) | Foundation | 📝 Ready |
| 03 | [AI Agent Core](docs/ai/guides/03-ai-agent-core.md) | Foundation | 📝 Ready |
| 04 | [Knowledge Base & RAG](docs/ai/guides/04-knowledge-base-rag.md) | Core Features | 📝 Ready |
| 05 | [Anonymous Reporting](docs/ai/guides/05-anonymous-reporting.md) | Core Features | 📝 Ready |
| 06 | [Query Escalation](docs/ai/guides/06-query-escalation.md) | Core Features | 📝 Ready |
| 07 | [Admin Dashboard](docs/ai/guides/07-admin-dashboard.md) | Core Features | 📝 Ready |
| 08 | [Voice Processing](docs/ai/guides/08-voice-processing.md) | Voice & Language | 📝 Ready |
| 09 | [Healthcare Agent](docs/ai/guides/09-healthcare-agent.md) | Extended | 📝 Ready |
| 10 | [Farmer Services](docs/ai/guides/10-farmer-services.md) | Extended | 📝 Ready |
| 11 | [Notifications](docs/ai/guides/11-notifications-profiling.md) | Extended | 📝 Ready |
| 12 | [WhatsApp](docs/ai/guides/12-whatsapp-integration.md) | Scale | 📝 Ready |
| 13 | [Performance](docs/ai/guides/13-scaling-performance.md) | Scale | 📝 Ready |

## Project Structure

```
src/janseva/
├── config.py          # Central configuration
├── bot/               # Telegram bot (aiogram)
├── agents/            # AI agents (LangGraph)
├── knowledge/         # Knowledge base & RAG
├── voice/             # Speech-to-Text / Text-to-Speech
├── admin/             # Admin dashboard (FastAPI)
├── reporting/         # Anonymous reporting engine
├── notifications/     # Notification system
├── db/                # Database models & repositories
└── common/            # Shared utilities
```

## License

Open source. Specific license TBD.
