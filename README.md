# JanSeva (जनसेवा)

An AI assistant that helps Indian citizens get government work done in the language they already speak.

Ask for an income certificate, a scheme they might qualify for, a nearby hospital, or today's mandi price. JanSeva answers in Hindi or English, on Telegram and on the web, and can file an anonymous report without storing who sent it.

## Highlights

- **One conversation, several specialists.** A LangGraph orchestrator classifies each message and routes it to service navigation, healthcare, farmer services, anonymous reporting, or escalation.
- **Answers grounded in a knowledge base.** Schemes, services, and subsidies live as YAML and are retrieved through a vector store before the model replies.
- **Hindi and English, text or voice.** The Telegram bot accepts text and voice notes. Speech-to-text uses Faster Whisper.
- **Anonymous reports with a tracking token.** Complaint text is stripped of obvious identifiers, encrypted, and returned with a token the citizen can use to check status. The report row has no user foreign key.
- **Two front doors.** A Next.js public site for citizens, and a FastAPI + HTMX admin console for officials. Admin assets are bundled locally so the console does not depend on a third-party CDN.

## Tech stack

| Layer | What it uses |
| --- | --- |
| Public site | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| API and admin | FastAPI, Jinja2, HTMX |
| Bot | aiogram 3 |
| Agents | LangGraph, LangChain, Gemini / OpenRouter / Ollama |
| Data | PostgreSQL 16, SQLAlchemy 2, Alembic, ChromaDB |
| Voice | Faster Whisper |
| Packaging | uv, Docker |

## What works today

- Telegram onboarding, text chat, and voice notes wired into the agent graph
- Specialist flows for service questions, healthcare lookup, farmer and mandi questions, escalation, and anonymous reports
- Knowledge ingestion from YAML, plus retrieval used by the service navigator
- Admin login, dashboard counts, organizations, users, queries, and report review
- Citizen web pages for services, schemes, institutions, chat, complaints, and anonymous reports
- Institution dashboards for a hospital and a police station, plus a department console
- Phone OTP and email login APIs, complaint and department APIs, and a Twilio WhatsApp webhook

## What is still incomplete

These are present in the tree, but they are stubs, demos, or not wired end to end:

- Mandi sync returns sample prices. The data.gov.in call is not implemented.
- Scheme alerts are scheduled, then do nothing.
- Location context only recognizes a handful of Uttar Pradesh and Madhya Pradesh districts.
- Several web screens use mock institutions, schemes, and dashboard numbers.
- Anonymous reports are not linked to an organization, so only a super admin can list them.
- WhatsApp delivery depends on Twilio credentials and a citizen row that already exists.
- There is no project license yet.

## Setup

Requires Python 3.11+, [uv](https://docs.astral.sh/uv/), Node.js 22, and a PostgreSQL database.

```bash
cp .env.example .env
# Set TELEGRAM_BOT_TOKEN and an LLM key (GOOGLE_API_KEY or OPENROUTER_API_KEY).
# Point DATABASE_URL and DATABASE_URL_SYNC at your Postgres instance.
# Use localhost when Postgres runs on the same machine.

uv sync --extra dev
uv run alembic upgrade head
uv run python scripts/seed_knowledge_base.py

uv run python -m janseva.bot.main
uv run uvicorn janseva.admin.app:admin_app --reload --port 8000
```

The public site:

```bash
cd web
npm ci
npm run dev
```

Open http://localhost:3000. The site calls the API at `NEXT_PUBLIC_API_URL`, defaulting to `http://localhost:8000/api`.

### Docker

`docker-compose.yml` builds the API/bot and the Next.js site and expects an external Postgres instance plus a `dokploy-network`. See [docs/deployment.md](docs/deployment.md). For a VPS without Dokploy, add the Caddy overlay:

```bash
docker compose -f docker-compose.yml -f docker-compose.standalone.yml up -d --build
```

## Checks

```bash
uv run ruff check .
uv run pytest -q
cd web && npm run lint && npm run build
```

GitHub Actions runs those commands on every push and pull request. `mypy` is configured with `strict = true` and still reports a large set of pre-existing annotation gaps, so it is not a CI gate yet.

## Suggested GitHub description

AI assistant for Indian government services: certificates, schemes, healthcare, and farmer help in Hindi and English.

Suggested topics: `civic-tech`, `india`, `government-services`, `langchain`, `langgraph`, `fastapi`, `nextjs`, `telegram-bot`, `rag`, `python`

## Docs

- [Project brief](docs/ai/00-project-brief.md)
- [Architecture](docs/ai/01-architecture.md)
- [Deployment](docs/deployment.md)
- [Knowledge base guide](docs/KNOWLEDGE_BASE_GENERATION_GUIDE.md)

## License

No license file yet. All rights reserved by the repository owner until one is added.
