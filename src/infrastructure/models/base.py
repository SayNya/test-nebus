import json
from typing import TypeVar

from pydantic import BaseModel, Extra, ConfigDict

__all__ = (
    "InternalModel",
    "_InternalModel",
    "PublicModel",
    "_PublicModel",
    "FrozenModel",
)


def to_camelcase(string: str) -> str:

    resp = "".join(
        word.capitalize() if index else word
        for index, word in enumerate(string.split("_"))
    )
    return resp




class FrozenModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class InternalModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        validate_default=True,
    )


_InternalModel = TypeVar("_InternalModel", bound=InternalModel)


class PublicModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True,
        alias_generator=to_camelcase,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    def encoded_dict(self, by_alias=True):
        return json.loads(self.model_dump_json(by_alias=by_alias))


_PublicModel = TypeVar("_PublicModel", bound=PublicModel)
