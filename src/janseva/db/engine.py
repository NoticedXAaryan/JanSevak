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
