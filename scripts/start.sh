#!/bin/bash
set -e

echo "Running database migrations..."
uv run alembic upgrade head

echo "Seeding knowledge base..."
uv run python scripts/seed_knowledge_base.py

echo "Starting Telegram bot..."
exec uv run python -m janseva.bot
