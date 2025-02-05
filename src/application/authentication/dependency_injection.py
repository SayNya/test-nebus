from fastapi import Depends
from fastapi.security import APIKeyHeader

from src.infrastructure.database import DBSessionDep
from src.infrastructure.errors import AuthenticationError
from src.domain.users import User, get_user_by_api_key

__all__ = ("get_current_user",)

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_current_user(
    db_session: DBSessionDep, api_key: str = Depends(api_key_header)
) -> User:
    user = await get_user_by_api_key(db_session, api_key)
    if not user:
        raise AuthenticationError
    return user
