#!/usr/bin/env bash
set -euo pipefail

# Use the venv binaries directly — DO NOT use "uv run" here.
# "uv run" triggers a re-sync that rebuilds the janseva package,
# producing a broken install that can't find submodules.
VENV_BIN="/app/.venv/bin"

if [[ "${RUN_MIGRATIONS:-true}" != "false" ]]; then
    echo "Running database migrations..."
    "$VENV_BIN/alembic" upgrade head
else
    echo "Skipping database migrations because RUN_MIGRATIONS=false"
fi

if [[ "${SEED_KNOWLEDGE_BASE:-true}" != "false" ]]; then
    echo "Seeding knowledge base if needed..."
    if "$VENV_BIN/python" scripts/seed_knowledge_base.py --skip-if-populated; then
        echo "Knowledge base seeding completed."
    else
        echo "WARNING: Knowledge base seeding failed. Bot will start without RAG data."
        echo "Set SEED_KNOWLEDGE_BASE=false to skip, or provide a valid GOOGLE_API_KEY for embeddings."
    fi
else
    echo "Skipping knowledge base seed because SEED_KNOWLEDGE_BASE=false"
fi

echo "Starting API Server..."
"$VENV_BIN/uvicorn" janseva.admin.app:admin_app --host 0.0.0.0 --port 8000 &

echo "Starting Telegram bot..."
exec "$VENV_BIN/python" -m janseva.bot
