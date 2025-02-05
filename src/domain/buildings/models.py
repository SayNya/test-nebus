from src.infrastructure.models import InternalModel, PublicModel

__all__ = ("Building", "BuildingPublic")


class _BuildingPublic(PublicModel):
    address: str


class BuildingPublic(_BuildingPublic):
    latitude: float
    longitude: float


class _BuildingInternal(InternalModel):
    address: str


class Building(_BuildingInternal):
    latitude: float
    longitude: float
