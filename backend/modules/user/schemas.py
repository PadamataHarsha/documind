"""User module schemas — request/response DTOs with Pydantic v2 validators."""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)
    roles: list[str] = Field(default_factory=list)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserUpdateRequest(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=255)
    avatar_url: str | None = None
    settings: dict[str, Any] | None = None


class UserRoleUpdateRequest(BaseModel):
    roles: list[str] = Field(min_length=1)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class RoleResponse(BaseModel):
    id: UUID
    name: str
    display_name: str
    description: str | None
    is_system: bool

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    email: str
    full_name: str
    avatar_url: str | None
    is_active: bool
    is_superadmin: bool
    email_verified: bool
    last_login_at: datetime | None
    roles: list[RoleResponse]
    settings: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int


class UserDeactivateRequest(BaseModel):
    reason: str | None = None
