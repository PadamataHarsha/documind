"""Audit repository — thin session wrapper over queries.audit."""
from __future__ import annotations  # `list()` method must not shadow list[...] hints

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models import AuditLog
from queries import count_from
from queries.audit import select_audit_logs


class AuditRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        *,
        tenant_id: UUID,
        actor_id: UUID | None,
        actor_type: str,
        action: str,
        resource_type: str,
        resource_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        request_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        status: str = "success",
    ) -> AuditLog:
        log = AuditLog(
            tenant_id=tenant_id,
            actor_id=actor_id,
            actor_type=actor_type,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            metadata_=metadata or {},
            status=status,
        )
        self.db.add(log)
        await self.db.flush()
        return log

    async def list(
        self,
        tenant_id: UUID,
        *,
        actor_id: UUID | None = None,
        action: str | None = None,
        resource_type: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[AuditLog], int]:
        base = select_audit_logs(
            tenant_id,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            since=since,
            until=until,
        )
        total = await count_from(self.db, base.subquery())
        result = await self.db.execute(base.limit(limit).offset(offset))
        return list(result.scalars().all()), total
