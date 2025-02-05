from src.infrastructure.models import InternalModel, PublicModel

__all__ = ("UserUncommited", "User", "UserRequestBody")


class _UserPublic(PublicModel):
    username: str


class UserRequestBody(_UserPublic):
    password: str


class _UserInternal(InternalModel):
    username: str


class UserUncommited(_UserInternal):
    password: str


class User(_UserInternal):
    id: int
