from fastapi import APIRouter, status

from src.application import users
from src.domain.api_keys import ApiKeyPublic
from src.domain.users import UserRequestBody, get_user_by_username
from src.infrastructure.database import DBSessionDep
from src.infrastructure.errors import ConflictError
from src.infrastructure.models import Response

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    summary="Регистрация",
    response_model=Response[ApiKeyPublic],
)
async def register(schema: UserRequestBody, db_session: DBSessionDep):
    """
    Регистрация пользователя:

    - **username**: Username пользователя
    - **password**: Пароль пользователя
    """
    existed_user = await get_user_by_username(db_session, schema.username)
    if existed_user:
        raise ConflictError(message="User with this username already exists")

    api_key = await users.register(db_session, payload=schema.model_dump())
    api_key_public = ApiKeyPublic.model_dump(api_key)

    return Response[ApiKeyPublic](result=api_key_public)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Логин",
    response_model=Response[ApiKeyPublic],
)
async def login(schema: UserRequestBody, db_session: DBSessionDep):
    """
    Авторизация пользователя:

    - **username**: Username пользователя
    - **password**: Пароль пользователя
    """
    api_key = await users.login(db_session, schema.model_dump())
    api_key_public = ApiKeyPublic.model_dump(api_key)
    return Response[ApiKeyPublic](result=api_key_public)
