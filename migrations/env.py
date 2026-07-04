"""Alembic environment configuration for async SQLAlchemy."""
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy import create_engine

import sys
from pathlib import Path

# Explicitly add src to python path for Docker/uv
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from janseva.db.models import Base  # Import Base to get all model metadata

# Alembic Config object
config = context.config

# Override sqlalchemy.url from env var if available (critical for Docker)
import os
db_url = os.environ.get("DATABASE_URL_SYNC")
if db_url:
    # Escape % to %% because configparser treats % as string interpolation
    escaped_url = db_url.replace("%", "%%")
    config.set_main_option("sqlalchemy.url", escaped_url)

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
