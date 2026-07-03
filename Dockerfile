FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    UV_LINK_MODE=copy

# Install system dependencies needed by database and vector-store wheels.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy the lockfile and pyproject.toml
COPY pyproject.toml uv.lock ./

# Install dependencies only (NOT the project itself).
# We rely on PYTHONPATH=/app/src for imports — no editable install needed.
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application source
COPY . .

# Verify the source code is importable via PYTHONPATH
RUN .venv/bin/python -c "\
import sys; print('sys.path:', sys.path); \
from janseva.db.models import Base; \
from janseva.config import Settings; \
print('All imports OK')"

# Setup entrypoint script
RUN chmod +x /app/scripts/start.sh

CMD ["/app/scripts/start.sh"]
