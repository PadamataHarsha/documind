"""Document module schemas — request/response DTOs."""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentUploadRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    custom_metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    uploaded_by: UUID
    title: str
    description: str | None
    file_name: str
    file_type: str
    mime_type: str
    file_size_bytes: int
    status: str
    tags: list[str]
    custom_metadata: dict[str, Any]
    page_count: int | None
    word_count: int | None
    language: str | None
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]
    total: int
    page: int
    page_size: int


class DocumentStatusResponse(BaseModel):
    id: UUID
    status: str
    progress: dict | None = None
    error_message: str | None = None


class DocumentUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    custom_metadata: dict[str, Any] | None = None
