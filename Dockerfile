FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    UV_LINK_MODE=copy

# Install system dependencies needed by database, vector-store wheels, and voice processing.
RUN apt-get update && apt-get install -y \
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
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application source
COPY . .

# DEBUG: List what actually got copied to find out what's missing
RUN echo "=== /app/src contents ===" && \
    find /app/src -type f -name "*.py" | head -50 && \
    echo "=== Looking for db/models ===" && \
    find /app/src -path "*/db/models*" && \
    echo "=== Full directory tree ===" && \
    find /app/src -type d | sort

# Setup entrypoint script
RUN chmod +x /app/scripts/start.sh

CMD ["/app/scripts/start.sh"]
