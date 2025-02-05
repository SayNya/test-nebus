from src.infrastructure.models import InternalModel, PublicModel

__all__ = ("PhoneNumber", "PhoneNumberPublic")


class _PhoneNumberPublic(PublicModel):
    phone_number: str


class PhoneNumberPublic(_PhoneNumberPublic):
    pass


class _PhoneNumberInternal(InternalModel):
    phone_number: str


class PhoneNumber(_PhoneNumberInternal):
    pass
