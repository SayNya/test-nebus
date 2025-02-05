import secrets
from pydantic import field_validator
from src.infrastructure.models import InternalModel, PublicModel

__all__ = ("ApiKeyUncommited", "ApiKey", "ApiKeyPublic")


class _ApiKeyPublic(PublicModel):
    key: str


class ApiKeyPublic(_ApiKeyPublic):
    pass


class _ApiKeyInternal(InternalModel):
    user_id: int


class ApiKeyUncommited(_ApiKeyInternal):
    key: str | None = None

    @field_validator("key", mode="before")
    @classmethod
    def set_key(cls, value):
        return value or secrets.token_hex(32)


class ApiKey(_ApiKeyInternal):
    id: int
    key: str
