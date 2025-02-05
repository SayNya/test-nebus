from src.infrastructure.models import InternalModel, PublicModel

__all__ = ("Activities", "ActivitiesPublic")


class _ActivitiesPublic(PublicModel):
    name: str


class ActivitiesPublic(_ActivitiesPublic):
    pass


class _ActivitiesInternal(InternalModel):
    name: str


class Activities(_ActivitiesInternal):
    pass
