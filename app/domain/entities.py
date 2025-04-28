from typing import Generic, TypeVar

from pydantic import BaseModel, NonNegativeInt, PositiveInt

T = TypeVar("T", bound="DomainModel")

DEFAULT_PAGINATION_LIMIT = 10


class DomainModel(BaseModel):
    id: str


class Pagination(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = DEFAULT_PAGINATION_LIMIT


class PaginatedResponse(BaseModel, Generic[T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]
