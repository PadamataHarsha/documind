"""Chat module schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationCreateRequest(BaseModel):
    title: str | None = None
    document_ids: list[UUID] = Field(default_factory=list)
    settings: dict[str, Any] = Field(default_factory=dict)


class ConversationResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    title: str | None
    summary: str | None
    document_ids: list[UUID]
    message_count: int
    token_count: int
    last_message_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationListResponse(BaseModel):
    items: list[ConversationResponse]
    total: int
    page: int
    page_size: int


class MessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=8000)
    metadata_filters: dict[str, Any] | None = None


class CitationSchema(BaseModel):
    index: int
    chunk_id: UUID
    document_id: UUID
    document_title: str
    document_filename: str
    page_number: int | None
    excerpt: str


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    citations: list[CitationSchema]
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    model_name: str | None
    latency_ms: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
