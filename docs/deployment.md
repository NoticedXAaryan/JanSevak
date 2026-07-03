# Deployment: CPU-only Dokploy/VPS

JanSeva is currently a Telegram polling bot. Deploy it as a worker/background service. Do not configure a public web port for the bot container.

## Required Dokploy settings

Use the Dockerfile or the included Compose file. The updated `docker-compose.yml` runs ONLY the bot service and connects to your **external managed PostgreSQL instance**. Redis has been dropped from the deployment architecture to save disk space and reduce complexity (the bot uses an in-memory dictionary for its rate limiter).

Required environment variables:

```env
TELEGRAM_BOT_TOKEN=replace-with-your-botfather-token
GOOGLE_API_KEY=replace-with-your-google-api-key
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash
EMBEDDING_PROVIDER=gemini
EMBEDDING_MODEL=models/embedding-001
ENV=production
LOG_LEVEL=INFO
RUN_MIGRATIONS=true
SEED_KNOWLEDGE_BASE=true
```

Database variables **must** point to your external managed PostgreSQL instance. Ensure you set both:

```env
# Must use postgresql+asyncpg:// for the asynchronous app code
DATABASE_URL=postgresql+asyncpg://user:password@your-postgres-host:5432/janseva
# Must use standard postgresql:// for Alembic synchronous migrations
DATABASE_URL_SYNC=postgresql://user:password@your-postgres-host:5432/janseva
```

> [!CAUTION]
> **Special Characters in Database Credentials**
> If your database username or password contains special characters like `@` or `#`, you **MUST URL-encode them**. 
> For example, a password of `Aaryan890@` must be written as `Aaryan890%40` in the URL. If you leave the raw `@` in the password, SQLAlchemy will wrongly interpret it as the start of the host name, causing `connection refused to socket` errors.

## CPU-only VPS rules

- Keep PyTorch, sentence-transformers, openai-whisper, CUDA wheels, and local LLM/voice models out of default production dependencies.
- Use cloud APIs for chat, embeddings, and speech on a basic VPS.
- Keep `.dockerignore` strict so `.venv`, `.env`, `.chromadb`, tests, docs, and caches are not uploaded into the Docker build context.
- Keep generated ChromaDB data in the Docker volume mounted at `/app/.chromadb`; do not commit `.chromadb/`.
- Keep `scripts/start.sh` with LF line endings. `.gitattributes` enforces this for future Windows edits.

> [!WARNING]
> **Gitignore & Dockerignore Paths (The `ModuleNotFoundError` Bug)**
> Be extremely careful with unanchored ignore paths. A previous bug caused `ModuleNotFoundError: No module named 'janseva.db.models'` inside Docker because `.gitignore` contained `models/`. This ignored *every* folder named `models` at any depth, stripping `src/janseva/db/models/` entirely from GitHub.
> **Rule:** Always use a leading slash (e.g., `/models/`) to anchor exclusions to the project root.

## First deploy checklist

1. Confirm `.env.example` has placeholders only. Never commit real bot tokens or API keys.
2. In Dokploy, set the required env vars above (remembering to URL-encode credentials).
3. Run the first deploy with `RUN_MIGRATIONS=true` and `SEED_KNOWLEDGE_BASE=true`.
4. After the first successful seed, the startup script skips seeding if Chroma already has documents.

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError` for application files | The files were excluded by an unanchored rule in `.gitignore` or `.dockerignore` | Anchor the rule (e.g. `/models/` instead of `models/`) and `git add` the missing files |
| `connection refused` / weird socket names | Unencoded `@` in the database password | Replace `@` with `%40` in `DATABASE_URL` and `DATABASE_URL_SYNC` |
| `uv sync` deletes package in Docker | Running `uv run` at container runtime | Run `.venv/bin/python` directly in `start.sh` instead of `uv run` |
| Disk fills during build | Local ML packages or build context copied into image | Do not add PyTorch/Whisper to base deps; keep `.dockerignore` intact |
| `/usr/bin/env: bash\r` or `bad interpreter` | CRLF shell script | Keep `.gitattributes`; recommit shell scripts with LF |
