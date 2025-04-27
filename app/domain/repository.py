from typing import Protocol, TypeVar

from app.domain.entities import DomainModel, PaginatedResponse, Pagination

T = TypeVar("T", bound=DomainModel)


class BaseRepositoryProtocol(Protocol[T]):
    def get_all(self, pagination: Pagination | None = None) -> PaginatedResponse[T]: ...
