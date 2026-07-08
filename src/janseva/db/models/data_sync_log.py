from sqlalchemy.orm import Mapped, mapped_column

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class DataSyncLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "data_sync_logs"

    source_name: Mapped[str] = mapped_column(index=True)
    status: Mapped[str] = mapped_column(index=True)  # "success", "failed", "partial"
    records_synced: Mapped[int] = mapped_column(default=0)
    error_message: Mapped[str | None]
    duration_seconds: Mapped[float]

    def __repr__(self) -> str:
        return f"<DataSyncLog {self.source_name} status={self.status}>"
