import logging
import time
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from janseva.db.engine import async_session_factory
from janseva.db.models.data_sync_log import DataSyncLog

logger = logging.getLogger(__name__)


class DataSource(ABC):
    """Base class for all external data sources in the sync engine."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def fetch_latest(self) -> list[dict[str, Any]]:
        """Fetch the latest data from the source."""
        pass

    @abstractmethod
    async def sync_to_db(self, session: AsyncSession, data: list[dict[str, Any]]) -> int:
        """
        Upsert fetched data into our database.
        Returns the number of records synced.
        """
        pass

    async def run_sync(self):
        """Full sync cycle with database logging."""
        logger.info(f"Starting sync for {self.name}")
        start_time = time.time()

        status = "failed"
        records_synced = 0
        error_message = None

        try:
            data = await self.fetch_latest()

            # Open a new session for the sync operation
            async with async_session_factory() as session:
                try:
                    records_synced = await self.sync_to_db(session, data)
                    await session.commit()
                    status = "success"
                except Exception as db_exc:
                    await session.rollback()
                    raise db_exc

        except Exception as e:
            logger.exception(f"Sync failed for {self.name}: {e}")
            error_message = str(e)
            status = "failed"

        finally:
            duration = time.time() - start_time
            logger.info(f"Completed sync for {self.name} in {duration:.2f}s. Status: {status}")

            # Log the result
            async with async_session_factory() as log_session:
                sync_log = DataSyncLog(
                    source_name=self.name,
                    status=status,
                    records_synced=records_synced,
                    error_message=error_message,
                    duration_seconds=duration,
                )
                log_session.add(sync_log)
                await log_session.commit()
