from src.domain.activities import Activities, ActivitiesPublic
from src.domain.buildings import Building, BuildingPublic
from src.domain.phone_numbers import PhoneNumber, PhoneNumberPublic
from src.infrastructure.models import InternalModel, PublicModel
from pydantic import model_validator
from fastapi import Depends

__all__ = ("Organization", "OrganizationPublic", "OrganizationSearchParams")


class _OrganizationPublic(PublicModel):
    name: str


class OrganizationPublic(_OrganizationPublic):
    phone_numbers: list[PhoneNumberPublic]
    building: BuildingPublic
    activities: list[ActivitiesPublic]


class _OrganizationInternal(InternalModel):
    name: str


class Organization(_OrganizationInternal):
    phone_numbers: list[PhoneNumber]
    building: Building
    activities: list[Activities]


class OrganizationSearchParams(InternalModel):
    building_address: str | None = None
    activity: str | None = None
    organization_name: str | None = None

    box_min_lat: float | None = None
    box_min_lon: float | None = None
    box_max_lat: float | None = None
    box_max_lon: float | None = None

    circle_lat: float | None = None
    circle_lon: float | None = None
    circle_rad: float | None = None

    @model_validator(mode="after")
    def validate_exclusive_fields(self):
        if any(
            (
                self.box_min_lat,
                self.box_min_lon,
                self.box_max_lat,
                self.box_max_lon,
            )
        ) and not all(
            (
                self.box_min_lat,
                self.box_min_lon,
                self.box_max_lat,
                self.box_max_lon,
            )
        ):
            raise ValueError("All box params should be provided")
        if any(
            (
                self.circle_lat,
                self.circle_lon,
                self.circle_rad,
            )
        ) and not all(
            (
                self.circle_lat,
                self.circle_lon,
                self.circle_rad,
            )
        ):
            raise ValueError("All circle params should be provided")
        if all(
            (
                self.box_min_lat,
                self.box_min_lon,
                self.box_max_lat,
                self.box_max_lon,
            )
        ) and all((self.circle_lat, self.circle_lon, self.circle_rad)):
            raise ValueError(
                "Only one of 'bounding_box' or 'bounding_circle' should be provided."
            )

        return self
