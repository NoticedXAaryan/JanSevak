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
    "$VENV_BIN/python" scripts/seed_knowledge_base.py --skip-if-populated
else
    echo "Skipping knowledge base seed because SEED_KNOWLEDGE_BASE=false"
fi

echo "Starting Admin Web Server..."
"$VENV_BIN/uvicorn" janseva.admin.app:admin_app --host 0.0.0.0 --port 8000 &

echo "Starting Telegram bot..."
exec "$VENV_BIN/python" -m janseva.bot
