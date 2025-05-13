from typing import Annotated, Generic, NewType, TypeVar

from pydantic import (
    BaseModel,
    BeforeValidator,
    NonNegativeInt,
    PositiveInt,
)

T = TypeVar("T", bound="DomainModel")
EntityId = NewType("EntityId", str)

ENTITY_ID_LENGTH = 24
DEFAULT_PAGINATION_LIMIT = 10


def validate_entity_id(value: str | None) -> str | None:
    if value is None:
        return None

    if len(value) != ENTITY_ID_LENGTH:
        raise ValueError(f"Must be {ENTITY_ID_LENGTH} characters long")

    try:
        bytes.fromhex(value)
        return value
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid entity id") from error


class DomainModel(BaseModel):
    id: Annotated[EntityId | None, BeforeValidator(validate_entity_id)]


class Pagination(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = DEFAULT_PAGINATION_LIMIT


class PaginatedResponse(BaseModel, Generic[T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
