#!/usr/bin/env bash
set -euo pipefail

if [[ "${RUN_MIGRATIONS:-true}" != "false" ]]; then
    echo "Running database migrations..."
    uv run alembic upgrade head
else
    echo "Skipping database migrations because RUN_MIGRATIONS=false"
fi

if [[ "${SEED_KNOWLEDGE_BASE:-true}" != "false" ]]; then
    echo "Seeding knowledge base if needed..."
    uv run python scripts/seed_knowledge_base.py --skip-if-populated
else
    echo "Skipping knowledge base seed because SEED_KNOWLEDGE_BASE=false"
fi

echo "Starting Telegram bot..."
exec uv run python -m janseva.bot
