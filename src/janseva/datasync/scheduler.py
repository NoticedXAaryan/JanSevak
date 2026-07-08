import asyncio
import logging

from janseva.datasync.base import DataSource
from janseva.datasync.sources.agmarknet import AgmarknetSource

logger = logging.getLogger(__name__)


class DataSyncScheduler:
    """Background scheduler for running data sync jobs."""

    def __init__(self):
        self.sources: list[DataSource] = [
            AgmarknetSource(),
            # Add more sources here (e.g., HealthHFRSource(), SchemesSource())
        ]
        self._running = False
        self._task = None

    async def start(self, interval_seconds: int = 3600):
        """Start the scheduler."""
        if self._running:
            return

        self._running = True
        logger.info(f"Starting Data Sync Scheduler (interval: {interval_seconds}s)")

        async def _run_loop():
            while self._running:
                for source in self.sources:
                    try:
                        await source.run_sync()
                    except Exception as e:
                        logger.error(f"Error running sync for {source.name}: {e}")

                # Sleep until next interval, checking for cancellation
                for _ in range(interval_seconds):
                    if not self._running:
                        break
                    await asyncio.sleep(1)

        self._task = asyncio.create_task(_run_loop())

    async def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._task:
            await self._task
            self._task = None
        logger.info("Data Sync Scheduler stopped")


# Global instance
scheduler = DataSyncScheduler()
