from typing import Any, ClassVar, Generic, TypeVar

from pymongo.database import Database

from app.domain.entities import DomainModel, PaginatedResponse, Pagination
from app.domain.repository import BaseRepositoryProtocol

T = TypeVar("T", bound=DomainModel)


class BaseRepository(BaseRepositoryProtocol[T], Generic[T]):
    domain_model: type[T]
    collection_name: ClassVar[str]

    def __init__(self, database: Database[dict[str, Any]]):
        self.database = database
        self.collection = self.database[self.collection_name]

    def _to_domain(self, doc: dict[str, Any]) -> T:
        doc["id"] = str(doc.pop("_id"))
        return self.domain_model.model_validate(doc)

    def get_all(self, pagination: Pagination | None = None) -> PaginatedResponse[T]:
        pagination = pagination or Pagination()
        skip = (pagination.page - 1) * pagination.limit

        total = self.collection.count_documents({})
        cursor = self.collection.find({}).skip(skip).limit(pagination.limit)
        items = [self._to_domain(doc) for doc in cursor]

        return PaginatedResponse(total=total, limit=pagination.limit, items=items)
