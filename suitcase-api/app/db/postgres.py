import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB, BYTEA
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum

from .base import Base

class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    ERROR = "error"
    DELETED = "deleted"

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

# For Legal Documents (Not Documents uploaded by Users)
class Document(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(100))
    doc_type: Mapped[str] = mapped_column(String(50))
    title: Mapped[Optional[str]] = mapped_column(String)
    content: Mapped[bytes] = mapped_column(BYTEA)
    # Metadata
    mdata: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    byte_size: Mapped[int] = mapped_column(Integer)
    status: Mapped[DocumentStatus] = mapped_column(SQLEnum(DocumentStatus))
    checksum: Mapped[str] = mapped_column(String(64))

class ScrapingJob(Base):
    __tablename__ = "scraping_jobs"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    batch_number: Mapped[int] = mapped_column(Integer)
    start_id: Mapped[int] = mapped_column(Integer)
    end_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[JobStatus] = mapped_column(SQLEnum(JobStatus))
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    error_details: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    worker_id: Mapped[UUID] = mapped_column(UUID)

class ScrapingMetric(Base):
    __tablename__ = "scraping_metrics"

    time: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    worker_id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    docs_processed: Mapped[int] = mapped_column(Integer)
    avg_response_time: Mapped[float] = mapped_column(Integer)
    rate_limit_hits: Mapped[int] = mapped_column(Integer)
    disk_usage_percent: Mapped[float] = mapped_column(Integer)
    memory_usage_mb: Mapped[int] = mapped_column(Integer)
    cpu_usage_percent: Mapped[float] = mapped_column(Integer)