# Deployment: CPU-only Dokploy/VPS

JanSeva is currently a Telegram polling bot. Deploy it as a worker/background service unless you also add and run an HTTP admin app. Do not configure a public web port for the bot container.

## Required Dokploy settings

Use the Dockerfile or the included Compose file. With the Compose file, `DATABASE_URL`, `DATABASE_URL_SYNC`, and `REDIS_URL` are generated from `POSTGRES_*`, `POSTGRES_HOST`, and `REDIS_HOST` so a local host-machine `.env` cannot accidentally inject `localhost` into the bot container.

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

Database and Redis variables must point to container/service hostnames, not `localhost`:

```env
DATABASE_URL=postgresql+asyncpg://janseva:password@postgres:5432/janseva
DATABASE_URL_SYNC=postgresql://janseva:password@postgres:5432/janseva
REDIS_URL=redis://redis:6379/0
```

If Dokploy provides managed Postgres or Redis, use the hostnames shown in the Dokploy service connection details. `localhost` inside the bot container means the bot container itself, not the database container.

For Compose deployments with managed services, set these instead of editing `DATABASE_URL` directly:

```env
POSTGRES_HOST=your-dokploy-postgres-host
POSTGRES_USER=janseva
POSTGRES_PASSWORD=your-password
POSTGRES_DB=janseva
REDIS_HOST=your-dokploy-redis-host
```

## CPU-only VPS rules

- Keep PyTorch, sentence-transformers, openai-whisper, CUDA wheels, and local LLM/voice models out of default production dependencies.
- Use cloud APIs for chat, embeddings, and speech on a basic VPS.
- Keep `.dockerignore` strict so `.venv`, `.env`, `.chromadb`, tests, docs, and caches are not uploaded into the Docker build context.
- Keep generated ChromaDB data in the Docker volume mounted at `/app/.chromadb`; do not commit `.chromadb/`.
- Keep `scripts/start.sh` with LF line endings. `.gitattributes` enforces this for future Windows edits.

## First deploy checklist

1. Confirm `.env.example` has placeholders only. Never commit real bot tokens or API keys.
2. In Dokploy, set the required env vars above.
3. Use `DATABASE_URL_SYNC` with the sync PostgreSQL scheme for Alembic migrations.
4. Run the first deploy with `RUN_MIGRATIONS=true` and `SEED_KNOWLEDGE_BASE=true`.
5. After the first successful seed, the startup script skips seeding if Chroma already has documents.

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| `connection refused` to Postgres | URL uses `localhost` inside Docker | Use the Postgres service hostname, usually `postgres` or Dokploy's internal host |
| Disk fills during build | Local ML packages or build context copied into image | Do not add PyTorch/Whisper to base deps; keep `.dockerignore` intact |
| `/usr/bin/env: bash\r` or `bad interpreter` | CRLF shell script | Keep `.gitattributes`; recommit shell scripts with LF |
| Bot deploys but no website opens | This service is a Telegram worker, not a web app | Deploy as worker/background service or add a separate HTTP admin service |
