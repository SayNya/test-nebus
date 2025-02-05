from typing import Annotated

from fastapi import APIRouter, status, Security, Depends

from src.application.authentication import get_current_user
from src.application import organizations
from src.domain.organizations import (
    get_organization_by_id,
    OrganizationPublic,
    OrganizationSearchParams,
)
from src.domain.users import User
from src.infrastructure.database import DBSessionDep
from src.infrastructure.errors import NotFoundError
from src.infrastructure.models import Response, ResponseMulti

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Поиск по параметрам",
    response_model=ResponseMulti[OrganizationPublic],
)
async def get_by_params(
    db_session: DBSessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["organizations"])],
    params: OrganizationSearchParams = Depends(),
):
    """
    Поиск организации по параметрам:
    - **building_address**: Адрес здания организации
    - **activity**: Деятельность организации
    - **organization_name**: Название организации

    - **box_min_lat**: Верхняя левая координата широты
    - **box_min_lon**: Верхняя левая координата долготы
    - **box_max_lat**: Нижняя правая координата широты
    - **box_max_lon**: Нижняя правая координата долготы

    - **circle_lat**: Координата широты точки центра окружности
    - **circle_lon**: Координата долготы точки центра окружности
    - **circle_rad**: Радиус окружности (км)

    Поиск по координатам может происходить, или по окружности, или по прямоугольной области (не 2 метода сразу)
    """
    organizations_iternal = await organizations.search_organizations_by_params(
        db_session, params
    )
    organizations_public = [
        OrganizationPublic.model_dump(org) for org in organizations_iternal
    ]
    return ResponseMulti[OrganizationPublic](result=organizations_public)


@router.get(
    "/{organization_id}",
    status_code=status.HTTP_200_OK,
    summary="Поиск по id",
    response_model=Response[OrganizationPublic],
)
async def get_by_id(
    organization_id: int,
    db_session: DBSessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["organizations"])],
):
    """
    Поиск организации по id:

    - **organization_id**: Идентификатор организации
    """
    organization = await get_organization_by_id(db_session, organization_id)
    if not organization:
        raise NotFoundError(message="Organization not found")
    organization_public = OrganizationPublic.model_dump(organization)
    return Response[OrganizationPublic](result=organization_public)
