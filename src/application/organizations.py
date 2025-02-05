from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.activities import get_activity_tree_ids
from src.domain.organizations import (
    OrganizationSearchParams,
    get_filtered_organizations,
    Organization,
)


async def search_organizations_by_params(
    db_session: AsyncSession, params: OrganizationSearchParams
) -> list[Organization]:
    filters = params.model_dump(exclude_none=True)

    if params.activity:
        activity_ids = await get_activity_tree_ids(db_session, params.activity)
        filters["activity_ids"] = activity_ids

    organizations = await get_filtered_organizations(db_session, filters)
    return organizations
