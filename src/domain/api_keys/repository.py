from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.api_keys import ApiKeyUncommited, ApiKey
from src.infrastructure.database import APIKeyTable

__all__ = ("create_api_key", "get_api_key")


async def create_api_key(db_session: AsyncSession, payload: ApiKeyUncommited) -> ApiKey:
    api_key = APIKeyTable(user_id=payload.user_id, key=payload.key)
    db_session.add(api_key)
    await db_session.commit()
    await db_session.flush()
    await db_session.refresh(api_key)
    return ApiKey.model_validate(api_key)


async def get_api_key(db_session: AsyncSession, user_id: int) -> ApiKey | None:
    api_key = (
        await db_session.scalars(
            select(APIKeyTable).where(APIKeyTable.user_id == user_id)
        )
    ).one_or_none()
    if not api_key:
        return None
    return ApiKey.model_validate(api_key)
