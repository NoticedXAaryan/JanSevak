FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    UV_LINK_MODE=copy

# Install system dependencies needed by database, vector-store wheels, and voice processing.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy the lockfile and pyproject.toml
COPY pyproject.toml uv.lock ./

# Install dependencies only (NOT the project itself).
RUN uv sync --frozen --no-install-project --no-dev --no-cache

# Copy the rest of the application source
COPY . .

# Setup entrypoint script
RUN chmod +x /app/scripts/start.sh

CMD ["/app/scripts/start.sh"]
