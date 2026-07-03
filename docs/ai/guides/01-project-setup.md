# Guide 01: Project Setup & Scaffolding

## What This Does
Creates the entire project structure, installs dependencies, sets up Docker services (PostgreSQL + Redis), initializes the database with Alembic migrations, and ensures everything runs correctly before writing any application logic.

## Prerequisites
- Python 3.11+ installed
- Docker Desktop installed and running
- Git initialized (`git init`)
- A terminal / command line

---

## Step 1: Initialize the Project with uv

`uv` is a fast Python package manager that replaces pip, pip-tools, and virtualenv.

```bash
# Install uv (if not already installed)
# On Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# On Linux/Mac:
# curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize the project (from the GoogleXParul directory)
uv init --name janseva --python 3.11
```

This creates a `pyproject.toml`. We'll replace its contents in the next step.

---

## Step 2: Create the Directory Structure

Create every directory and file listed below. Empty `__init__.py` files are required for Python to treat directories as packages.

```
GoogleXParul/
├── .env.example                 # Template for environment variables
├── .env                         # Actual env vars (NEVER commit this)
├── .gitignore                   # Git ignore rules
├── pyproject.toml               # Project config & dependencies
├── uv.lock                     # Auto-generated lockfile (DO commit)
├── docker-compose.yml           # PostgreSQL + Redis services
├── alembic.ini                  # Alembic migration config
├── README.md                    # Project README
│
├── docs/                        # Documentation (already created)
│   └── ai/
│       ├── 00-project-brief.md
│       ├── 01-architecture.md
│       ├── 02-active-context.md
│       ├── 03-implementation-master.md
│       └── guides/
│           ├── 01-project-setup.md       (this file)
│           ├── 02-telegram-bot.md
│           └── ...
│
├── src/                         # All application source code
│   └── janseva/
│       ├── __init__.py
│       │
│       ├── config.py            # Central configuration (reads .env)
│       │
│       ├── db/                  # Database layer
│       │   ├── __init__.py
│       │   ├── engine.py        # SQLAlchemy async engine & session
│       │   ├── models/          # SQLAlchemy ORM models
│       │   │   ├── __init__.py
│       │   │   ├── base.py      # Declarative base + common mixins
│       │   │   ├── user.py
│       │   │   ├── conversation.py
│       │   │   ├── message.py
│       │   │   ├── anonymous_report.py
│       │   │   ├── escalated_query.py
│       │   │   ├── service_catalog.py
│       │   │   └── authority.py
│       │   └── repositories/    # Data access layer (queries)
│       │       ├── __init__.py
│       │       ├── user_repo.py
│       │       ├── conversation_repo.py
│       │       └── report_repo.py
│       │
│       ├── bot/                 # Telegram bot layer
│       │   ├── __init__.py
│       │   ├── main.py          # Bot entry point (polling/webhook)
│       │   ├── routers/         # aiogram routers (like FastAPI routers)
│       │   │   ├── __init__.py
│       │   │   ├── start.py     # /start, /help commands
│       │   │   ├── text.py      # Text message handler
│       │   │   ├── voice.py     # Voice message handler
│       │   │   └── report.py    # Anonymous report flow
│       │   ├── middlewares/     # aiogram middlewares
│       │   │   ├── __init__.py
│       │   │   ├── session.py   # User session / DB session
│       │   │   └── throttle.py  # Rate limiting
│       │   └── keyboards/      # Inline/reply keyboard builders
│       │       ├── __init__.py
│       │       └── menus.py
│       │
│       ├── agents/              # AI Agent layer (LangGraph)
│       │   ├── __init__.py
│       │   ├── orchestrator.py  # Main orchestrator agent
│       │   ├── state.py         # LangGraph state definitions
│       │   ├── specialists/     # Specialist agents
│       │   │   ├── __init__.py
│       │   │   ├── service_navigator.py
│       │   │   ├── anonymous_reporter.py
│       │   │   ├── healthcare.py
│       │   │   ├── farmer_services.py
│       │   │   ├── escalation.py
│       │   │   └── notification.py
│       │   └── tools/           # Agent tools (functions agents can call)
│       │       ├── __init__.py
│       │       ├── knowledge_search.py
│       │       ├── form_generator.py
│       │       ├── facility_search.py
│       │       └── subsidy_checker.py
│       │
│       ├── voice/               # Voice processing layer
│       │   ├── __init__.py
│       │   ├── stt.py           # Speech-to-Text service
│       │   ├── tts.py           # Text-to-Speech service
│       │   └── audio_utils.py   # Audio format conversion
│       │
│       ├── knowledge/           # Knowledge base & RAG
│       │   ├── __init__.py
│       │   ├── embeddings.py    # Embedding model setup
│       │   ├── vector_store.py  # ChromaDB / pgvector interface
│       │   ├── ingestion.py     # Document ingestion pipeline
│       │   └── data/            # Raw knowledge base data
│       │       ├── services/    # Government service YAML files
│       │       ├── subsidies/   # Farm subsidy data
│       │       └── healthcare/  # Healthcare facility data
│       │
│       ├── admin/               # Admin dashboard
│       │   ├── __init__.py
│       │   ├── app.py           # FastAPI admin app
│       │   ├── auth.py          # Admin authentication
│       │   ├── routes/          # Admin API routes
│       │   │   ├── __init__.py
│       │   │   ├── dashboard.py
│       │   │   ├── queries.py
│       │   │   ├── reports.py
│       │   │   └── catalog.py
│       │   ├── templates/       # Jinja2 HTML templates
│       │   │   ├── base.html
│       │   │   ├── login.html
│       │   │   ├── dashboard.html
│       │   │   ├── queries.html
│       │   │   └── reports.html
│       │   └── static/          # CSS, JS for admin
│       │       ├── style.css
│       │       └── htmx.min.js
│       │
│       ├── reporting/           # Anonymous reporting engine
│       │   ├── __init__.py
│       │   ├── anonymizer.py    # Metadata stripping
│       │   ├── router.py        # Authority routing logic
│       │   ├── encryption.py    # Report encryption at rest
│       │   └── tokens.py        # Anonymous report token system
│       │
│       ├── notifications/       # Notification engine
│       │   ├── __init__.py
│       │   ├── engine.py        # Notification dispatch
│       │   ├── profiler.py      # Interest profiling
│       │   └── scheduler.py     # Scheduled notification jobs
│       │
│       └── common/              # Shared utilities
│           ├── __init__.py
│           ├── channel.py       # Channel normalizer (Telegram/WhatsApp → unified)
│           ├── logging.py       # Structured logging setup
│           └── exceptions.py    # Custom exception classes
│
├── migrations/                  # Alembic migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/               # Migration files go here
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Shared test fixtures
│   ├── test_agents/
│   │   ├── __init__.py
│   │   └── test_orchestrator.py
│   ├── test_bot/
│   │   ├── __init__.py
│   │   └── test_handlers.py
│   └── test_reporting/
│       ├── __init__.py
│       └── test_anonymizer.py
│
└── scripts/                     # Utility scripts
    ├── seed_knowledge_base.py   # Populate knowledge base with initial data
    ├── seed_authorities.py      # Populate authority hierarchy
    └── create_admin.py          # Create the first admin user
```

**To create this structure**, run:

```bash
# From the GoogleXParul directory

# Source code directories
mkdir -p src/janseva/db/models
mkdir -p src/janseva/db/repositories
mkdir -p src/janseva/bot/routers
mkdir -p src/janseva/bot/middlewares
mkdir -p src/janseva/bot/keyboards
mkdir -p src/janseva/agents/specialists
mkdir -p src/janseva/agents/tools
mkdir -p src/janseva/voice
mkdir -p src/janseva/knowledge/data/services
mkdir -p src/janseva/knowledge/data/subsidies
mkdir -p src/janseva/knowledge/data/healthcare
mkdir -p src/janseva/admin/routes
mkdir -p src/janseva/admin/templates
mkdir -p src/janseva/admin/static
mkdir -p src/janseva/reporting
mkdir -p src/janseva/notifications
mkdir -p src/janseva/common

# Migrations
mkdir -p migrations/versions

# Tests
mkdir -p tests/test_agents
mkdir -p tests/test_bot
mkdir -p tests/test_reporting

# Scripts
mkdir -p scripts
```

Then create all `__init__.py` files:

```bash
# Create all __init__.py files
# On Windows PowerShell:
$dirs = @(
    "src/janseva",
    "src/janseva/db",
    "src/janseva/db/models",
    "src/janseva/db/repositories",
    "src/janseva/bot",
    "src/janseva/bot/routers",
    "src/janseva/bot/middlewares",
    "src/janseva/bot/keyboards",
    "src/janseva/agents",
    "src/janseva/agents/specialists",
    "src/janseva/agents/tools",
    "src/janseva/voice",
    "src/janseva/knowledge",
    "src/janseva/admin",
    "src/janseva/admin/routes",
    "src/janseva/reporting",
    "src/janseva/notifications",
    "src/janseva/common",
    "tests",
    "tests/test_agents",
    "tests/test_bot",
    "tests/test_reporting"
)
foreach ($dir in $dirs) {
    New-Item -ItemType File -Path "$dir/__init__.py" -Force
}
```

---

## Step 3: Create pyproject.toml

Replace the auto-generated `pyproject.toml` with:

```toml
[project]
name = "janseva"
version = "0.1.0"
description = "AI-powered government services platform for Indian citizens"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    # --- Telegram Bot ---
    "aiogram>=3.15,<4",
    
    # --- Web Framework ---
    "fastapi>=0.115,<1",
    "uvicorn[standard]>=0.32,<1",
    "jinja2>=3.1,<4",
    "python-multipart>=0.0.12",
    
    # --- AI / LLM ---
    "langgraph>=0.2,<1",
    "langchain>=0.3,<1",
    "langchain-google-genai>=2,<3",       # Gemini API
    "langchain-community>=0.3,<1",
    
    # --- Database ---
    "sqlalchemy[asyncio]>=2.0,<3",
    "asyncpg>=0.30,<1",                    # Async PostgreSQL driver
    "alembic>=1.14,<2",
    "greenlet>=3.1,<4",                    # Required by SQLAlchemy async
    
    # --- Cache / Queue ---
    "redis[hiredis]>=5.2,<6",
    "arq>=0.26,<1",
    
    # --- Vector Store (RAG) ---
    "chromadb>=0.5,<1",
    
    # --- Voice Processing ---
    "pydub>=0.25,<1",
    # Do not add openai-whisper/PyTorch to default deps for CPU-only VPS deploys.
    # Use a cloud STT API or an optional local-voice extra when voice is implemented.
    
    # --- Security ---
    "cryptography>=43,<44",                # Report encryption
    "python-jose[cryptography]>=3.3,<4",   # JWT for admin auth
    "passlib[bcrypt]>=1.7,<2",             # Password hashing
    
    # --- Utilities ---
    "pydantic>=2.9,<3",
    "pydantic-settings>=2.6,<3",
    "structlog>=24,<26",
    "httpx>=0.27,<1",
    "python-dotenv>=1.0,<2",
    "langdetect>=1.0,<2",
]

[project.optional-dependencies]
dev = [
    "pytest>=8,<9",
    "pytest-asyncio>=0.24,<1",
    "pytest-cov>=6,<7",
    "ruff>=0.8,<1",
    "mypy>=1.13,<2",
    "pre-commit>=4,<5",
]

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---

## Step 4: Create .env.example and .env

**.env.example** (committed to git — template for others):

```env
# ============================================
# JanSeva Environment Configuration
# ============================================
# Copy this file to .env and fill in the values.
# NEVER commit .env to git.

# --- Telegram ---
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here

# --- Database ---
DATABASE_URL=postgresql+asyncpg://janseva:janseva_dev@localhost:5432/janseva
DATABASE_URL_SYNC=postgresql://janseva:janseva_dev@localhost:5432/janseva

# --- Redis ---
REDIS_URL=redis://localhost:6379/0

# --- LLM ---
# Option 1: Google Gemini (recommended for production)
GOOGLE_API_KEY=your-google-api-key-here
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash

# Option 2: Ollama (for local development without API costs)
# LLM_PROVIDER=ollama
# LLM_MODEL=llama3.1
# OLLAMA_BASE_URL=http://localhost:11434

# --- Security ---
ADMIN_JWT_SECRET=change-this-to-a-random-64-char-string
REPORT_ENCRYPTION_KEY=change-this-to-a-fernet-key

# --- Admin ---
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-this-in-production

# --- Voice (optional for Phase 3) ---
# WHISPER_MODEL_SIZE=large-v3
# INDICWHISPER_MODEL_PATH=./models/indicwhisper

# --- App ---
ENV=development
LOG_LEVEL=DEBUG
```

**.env** — Copy `.env.example` to `.env` and fill in real values. At minimum, you need:
- `TELEGRAM_BOT_TOKEN` (get from @BotFather on Telegram)
- `GOOGLE_API_KEY` (get from Google AI Studio) OR set `LLM_PROVIDER=ollama` for local dev

---

## Step 5: Create .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/
.eggs/

# Virtual environments
.venv/
venv/
env/

# Environment variables
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker volumes
pgdata/
redisdata/

# Models (large files)
models/

# Logs
*.log
logs/

# Test / Coverage
.coverage
htmlcov/
.pytest_cache/

# Build
*.egg
*.whl

# Alembic
migrations/versions/__pycache__/
```

---

## Step 6: Create docker-compose.yml

```yaml
# docker-compose.yml
# Runs PostgreSQL and Redis for local development.
# Usage: docker compose up -d

services:
  postgres:
    image: postgres:16-alpine
    container_name: janseva-postgres
    environment:
      POSTGRES_USER: janseva
      POSTGRES_PASSWORD: janseva_dev
      POSTGRES_DB: janseva
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U janseva"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: janseva-redis
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
  redisdata:
```

---

## Step 7: Create the Configuration Module

**File: `src/janseva/config.py`**

```python
"""
Central configuration module.
Reads all settings from environment variables (.env file).
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- Telegram ---
    telegram_bot_token: str = Field(..., description="Telegram bot token from BotFather")

    # --- Database ---
    database_url: str = Field(
        "postgresql+asyncpg://janseva:janseva_dev@localhost:5432/janseva",
        description="Async PostgreSQL connection string",
    )
    database_url_sync: str = Field(
        "postgresql://janseva:janseva_dev@localhost:5432/janseva",
        description="Sync PostgreSQL connection string (for Alembic)",
    )

    # --- Redis ---
    redis_url: str = Field("redis://localhost:6379/0")

    # --- LLM ---
    google_api_key: str = Field("", description="Google Gemini API key")
    llm_provider: str = Field("gemini", description="LLM provider: 'gemini' or 'ollama'")
    llm_model: str = Field("gemini-2.0-flash", description="LLM model name")
    ollama_base_url: str = Field("http://localhost:11434")

    # --- Security ---
    admin_jwt_secret: str = Field("change-me", description="JWT secret for admin auth")
    report_encryption_key: str = Field("change-me", description="Fernet key for report encryption")

    # --- Admin ---
    admin_username: str = Field("admin")
    admin_password: str = Field("change-me")

    # --- App ---
    env: str = Field("development")
    log_level: str = Field("DEBUG")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton instance — import this everywhere
settings = Settings()
```

---

## Step 8: Create the Database Engine

**File: `src/janseva/db/engine.py`**

```python
"""
SQLAlchemy async engine and session factory.
"""
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from janseva.config import settings

# Create the async engine
engine = create_async_engine(
    settings.database_url,
    echo=(settings.env == "development"),  # SQL logging in dev
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
)

# Session factory — use this to create sessions
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """Dependency for getting a database session."""
    async with async_session_factory() as session:
        yield session
```

---

## Step 9: Create the Base Model & Initial ORM Models

**File: `src/janseva/db/models/base.py`**

```python
"""
SQLAlchemy declarative base with common mixins.
Every model inherits from Base and gets id, created_at, updated_at for free.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class TimestampMixin:
    """Adds created_at and updated_at columns to any model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    """Adds a UUID primary key column."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
```

**File: `src/janseva/db/models/user.py`**

```python
"""User model — represents a citizen using JanSeva."""
from sqlalchemy import BigInteger, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    telegram_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="hi", nullable=False)
    district: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)
    interests: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relationships
    conversations = relationship("Conversation", back_populates="user", lazy="selectin")
```

**File: `src/janseva/db/models/conversation.py`**

```python
"""Conversation model — a session between a user and the AI agent."""
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Conversation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "conversations"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    agent_type: Mapped[str] = mapped_column(
        String(50), default="orchestrator", nullable=False
    )
    state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default="active", nullable=False
    )  # active, completed, escalated

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", lazy="selectin")
```

**File: `src/janseva/db/models/message.py`**

```python
"""Message model — individual messages in a conversation."""
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Message(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(
        String(10), nullable=False
    )  # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="hi", nullable=False)
    voice_audio_ref: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
```

**File: `src/janseva/db/models/__init__.py`**

```python
"""Export all models so Alembic can auto-detect them."""
from janseva.db.models.base import Base
from janseva.db.models.user import User
from janseva.db.models.conversation import Conversation
from janseva.db.models.message import Message

__all__ = ["Base", "User", "Conversation", "Message"]
```

---

## Step 10: Set Up Alembic Migrations

```bash
# From the GoogleXParul directory, initialize Alembic:
uv run alembic init migrations
```

This creates `alembic.ini` and `migrations/` directory. Now edit two files:

**Edit `alembic.ini`** — Find the `sqlalchemy.url` line and change it:

```ini
# alembic.ini
sqlalchemy.url = postgresql://janseva:janseva_dev@localhost:5432/janseva
```

**Replace `migrations/env.py`** with:

```python
"""Alembic environment configuration for async SQLAlchemy."""
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy import create_engine

from janseva.db.models import Base  # Import Base to get all model metadata

# Alembic Config object
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## Step 11: Create the Structured Logging Setup

**File: `src/janseva/common/logging.py`**

```python
"""Structured logging configuration using structlog."""
import logging
import structlog

from janseva.config import settings


def setup_logging() -> None:
    """Configure structured JSON logging for the entire application."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            # In dev: pretty console output. In prod: JSON.
            structlog.dev.ConsoleRenderer()
            if settings.env == "development"
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
```

---

## Step 12: Install Dependencies & Verify

```bash
# Install all dependencies
uv sync

# Install dev dependencies too
uv sync --extra dev

# Start Docker services
docker compose up -d

# Wait 5 seconds for PostgreSQL to be ready, then:
# Create the first migration
uv run alembic revision --autogenerate -m "initial schema: users, conversations, messages"

# Apply the migration
uv run alembic upgrade head
```

---

## Verification Checklist

- [ ] `docker compose ps` shows both `janseva-postgres` and `janseva-redis` running and healthy
- [ ] `uv run alembic upgrade head` completes without errors
- [ ] Connecting to PostgreSQL (`psql -h localhost -U janseva -d janseva`) shows the `users`, `conversations`, and `messages` tables
- [ ] `uv run python -c "from janseva.config import settings; print(settings.env)"` prints `development`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `uv: command not found` | Re-run the uv install command, restart terminal |
| `docker compose` fails | Ensure Docker Desktop is running. On Windows, check WSL2 is enabled |
| Alembic can't connect to DB | Ensure PostgreSQL container is running (`docker compose up -d postgres`), check the URL in `alembic.ini` matches your Docker config |
| `ModuleNotFoundError: janseva` | Make sure you're running commands from the `GoogleXParul` directory and that `src/janseva/__init__.py` exists |
| Port 5432 already in use | Another PostgreSQL is running. Stop it or change the port in `docker-compose.yml` |
| Docker/Dokploy cannot reach Postgres or Redis | Inside containers, use service hostnames like `postgres` and `redis`, not `localhost` |
| VPS runs out of disk during Docker build | Keep PyTorch, Whisper, CUDA, `.venv/`, and `.chromadb/` out of the production image and build context |
| Bot deploys but no website opens | The current app is a Telegram polling worker, not an HTTP web service |

---

## Git Checkpoint

After completing this step:

```bash
git add -A
git commit -m "chore(setup): scaffold project structure, Docker services, initial DB schema

- Initialize project with uv + pyproject.toml
- Create full directory structure for all application layers
- Docker Compose: PostgreSQL 16 + Redis 7
- SQLAlchemy async models: User, Conversation, Message
- Alembic migration setup with auto-detection
- Centralized config via pydantic-settings
- Structured logging via structlog"
```
