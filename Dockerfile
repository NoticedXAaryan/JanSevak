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

# Install dependencies (without the project itself — source isn't copied yet)
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application
COPY . .

# Install the project itself (force reinstall to avoid stale cache)
RUN uv sync --frozen --no-dev --reinstall-package janseva

# Verify the package installed correctly (fail the build early if broken)
RUN .venv/bin/python -c "from janseva.db.models import Base; print('Package verification OK:', Base)"

# Setup entrypoint script
RUN chmod +x /app/scripts/start.sh

# Run the startup script
CMD ["/app/scripts/start.sh"]
