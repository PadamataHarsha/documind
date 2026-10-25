"""Ingestion module schemas — ingestion job tracking DTOs."""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class IngestionJobResponse(BaseModel):
    id: UUID
    document_id: UUID
    job_type: str
    status: str
    celery_task_id: str | None
    attempt_count: int
    max_attempts: int
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None
    progress: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}


class IngestionJobListResponse(BaseModel):
    items: list[IngestionJobResponse]
    total: int
    page: int
    page_size: int
