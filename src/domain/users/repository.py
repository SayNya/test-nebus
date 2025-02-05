from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users import UserUncommited, User
from src.infrastructure.database import UserTable, APIKeyTable

__all__ = (
    "get_user_by_username",
    "create_user",
    "get_user_by_api_key",
    "get_user_by_password",
)

from src.infrastructure.errors import AuthenticationError


async def get_user_by_username(db_session: AsyncSession, username: str) -> User | None:
    user = (
        await db_session.scalars(
            select(UserTable).where(UserTable.username == username)
        )
    ).one_or_none()
    if user:
        return User.model_validate(user)
    return None


async def create_user(db_session: AsyncSession, payload: UserUncommited) -> User:
    user = UserTable(username=payload.username)
    user.set_password(payload.password)
    db_session.add(user)
    await db_session.commit()
    await db_session.flush()
    await db_session.refresh(user)
    return User.model_validate(user)


async def get_user_by_api_key(db_session: AsyncSession, key: str) -> User | None:
    user = (
        await db_session.scalars(
            select(UserTable).where(
                UserTable.id == APIKeyTable.user_id, APIKeyTable.key == key
            )
        )
    ).one_or_none()
    if user:
        return User.model_validate(user)
    return None


async def get_user_by_password(
    db_session: AsyncSession, payload: UserUncommited
) -> User | None:
    user = (
        await db_session.scalars(
            select(UserTable).where(UserTable.username == payload.username)
        )
    ).one_or_none()

    if not user:
        return None

    if not user.check_password(payload.password):
        raise AuthenticationError(message="Wrong password")

    return User.model_validate(user)
