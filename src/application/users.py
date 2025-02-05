from src.domain.api_keys import ApiKeyUncommited, ApiKey, create_api_key, get_api_key
from src.domain.users import UserUncommited, create_user, get_user_by_password
from src.infrastructure.errors import NotFoundError
from sqlalchemy.ext.asyncio import AsyncSession


async def register(db_session: AsyncSession, payload: dict) -> ApiKey:
    user = await create_user(db_session, UserUncommited(**payload))
    api_key = await create_api_key(db_session, ApiKeyUncommited(user_id=user.id))

    return api_key


async def login(db_session: AsyncSession, payload: dict) -> ApiKey:
    user = await get_user_by_password(db_session, UserUncommited(**payload))
    if not user:
        raise NotFoundError(message="User with that username not found")
    api_key = await get_api_key(db_session, user.id)
    if not api_key:
        return await create_api_key(db_session, ApiKeyUncommited(user_id=user.id))
    return api_key
