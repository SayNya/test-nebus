from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.organizations import Organization
from src.infrastructure.database import OrganizationTable, BuildingTable, ActivityTable

__all__ = ("get_organization_by_id", "get_filtered_organizations")


async def get_organization_by_id(
    db_session: AsyncSession, organization_id: int
) -> Organization | None:
    organization = (
        await db_session.scalars(
            select(OrganizationTable)
            .where(OrganizationTable.id == organization_id)
            .options(
                selectinload(
                    OrganizationTable.building,
                ),
                selectinload(
                    OrganizationTable.activities,
                ),
                selectinload(
                    OrganizationTable.phone_numbers,
                ),
            )
        )
    ).one_or_none()
    if organization:
        return Organization.model_validate(organization)
    return None


async def get_filtered_organizations(
    db_session: AsyncSession, filters: dict
) -> list[Organization]:

    query = select(OrganizationTable)

    if "building_address" in filters:
        query = query.where(
            OrganizationTable.building_id == BuildingTable.id,
            BuildingTable.address == filters["building_address"],
        )

    if "activity_ids" in filters:
        query = query.where(
            OrganizationTable.activities.any(
                ActivityTable.id.in_(filters["activity_ids"])
            )
        )

    if "organization_name" in filters:
        query = query.where(
            OrganizationTable.name.ilike(f"%{filters['organization_name']}%")
        )

    if "circle_rad" in filters:
        lat = filters["circle_lat"]
        lon = filters["circle_lon"]
        radius = filters["circle_rad"]

        query = query.where(
            OrganizationTable.building_id == BuildingTable.id,
            func.acos(
                func.cos(func.radians(lat))
                * func.cos(func.radians(BuildingTable.latitude))
                * func.cos(func.radians(BuildingTable.longitude) - func.radians(lon))
                + func.sin(func.radians(lat))
                * func.sin(func.radians(BuildingTable.latitude))
            )
            * 6371
            <= radius,
        )

    if "box_min_lat" in filters:
        min_lat = filters["box_min_lat"]
        min_lon = filters["box_min_lon"]
        max_lat = filters["box_max_lat"]
        max_lon = filters["box_max_lon"]

        query = query.where(
            OrganizationTable.building_id == BuildingTable.id,
            BuildingTable.latitude.between(min_lat, max_lat),
            BuildingTable.longitude.between(min_lon, max_lon),
        )
    query = query.options(
        selectinload(
            OrganizationTable.building,
        ),
        selectinload(
            OrganizationTable.activities,
        ),
        selectinload(
            OrganizationTable.phone_numbers,
        ),
    )

    organizations = (await db_session.scalars(query)).all()
    return [Organization.model_validate(organization) for organization in organizations]
