"""Webhook module schemas."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator

# Events a webhook may subscribe to (mirrors integrations.events.Events).
ALLOWED_EVENTS = {
    "document.uploaded",
    "document.ready",
    "document.failed",
    "document.deleted",
}


class WebhookCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    url: AnyHttpUrl
    events: list[str] = Field(min_length=1)

    @field_validator("events")
    @classmethod
    def validate_events(cls, v: list[str]) -> list[str]:
        invalid = [e for e in v if e not in ALLOWED_EVENTS]
        if invalid:
            raise ValueError(f"Unknown events: {', '.join(invalid)}")
        return v


class WebhookUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    url: AnyHttpUrl | None = None
    events: list[str] | None = None
    is_active: bool | None = None

    @field_validator("events")
    @classmethod
    def validate_events(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        invalid = [e for e in v if e not in ALLOWED_EVENTS]
        if invalid:
            raise ValueError(f"Unknown events: {', '.join(invalid)}")
        return v


class WebhookResponse(BaseModel):
    id: UUID
    name: str
    url: str
    events: list[str]
    is_active: bool
    failure_count: int
    last_success_at: datetime | None
    last_failure_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class WebhookCreatedResponse(WebhookResponse):
    """Returned once on creation — includes the signing secret."""
    secret: str


class WebhookListResponse(BaseModel):
    items: list[WebhookResponse]
    total: int
