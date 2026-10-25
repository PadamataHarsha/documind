"""User repository — thin session wrapper over queries.users."""
# This class defines a `list()` method which shadows the builtin `list` inside
# its own type hints, so the annotations below use typing.List instead.
from __future__ import annotations

import builtins
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from queries import count_from
from queries.users import (
    delete_user_role_associations,
    insert_user_role,
    select_roles_by_names,
    select_user,
    select_user_by_email,
    select_users,
    soft_delete_user,
    update_user_fields,
)


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: UUID, tenant_id: UUID) -> User | None:
        result = await self.db.execute(select_user(user_id, tenant_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str, tenant_id: UUID) -> User | None:
        result = await self.db.execute(select_user_by_email(email, tenant_id))
        return result.scalar_one_or_none()

    async def list(
        self,
        tenant_id: UUID,
        *,
        is_active: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[builtins.list[User], int]:
        base = select_users(tenant_id, is_active=is_active)
        total = await count_from(self.db, base.subquery())
        result = await self.db.execute(base.limit(limit).offset(offset))
        return list(result.scalars().all()), total

    async def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user, ["roles"])
        return user

    async def update(self, user_id: UUID, tenant_id: UUID, **kwargs) -> User | None:
        await self.db.execute(update_user_fields(user_id, tenant_id, **kwargs))
        return await self.get_by_id(user_id, tenant_id)

    async def soft_delete(self, user_id: UUID, tenant_id: UUID) -> bool:
        result = await self.db.execute(soft_delete_user(user_id, tenant_id))
        return result.rowcount > 0

    async def set_roles(self, user_id: UUID, tenant_id: UUID, role_names: builtins.list[str]) -> None:
        """Replace all role associations for a user."""
        roles_result = await self.db.execute(select_roles_by_names(role_names))
        roles = roles_result.scalars().all()

        await self.db.execute(delete_user_role_associations(user_id))
        for role in roles:
            await self.db.execute(insert_user_role(user_id, role.id))
        await self.db.flush()

    async def refresh_roles(self, user: User) -> None:
        await self.db.refresh(user, attribute_names=["roles"])
