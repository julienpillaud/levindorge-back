from typing import Any, ClassVar, Generic, TypeVar

from bson import ObjectId
from pymongo.database import Database

from app.domain.entities import DomainModel, EntityId, PaginatedResponse, Pagination
from app.domain.repository import BaseRepositoryProtocol

T = TypeVar("T", bound=DomainModel)
type MongoDocument = dict[str, Any]


def to_domain_entity(model: type[T], document: MongoDocument) -> T:
    document["id"] = str(document.pop("_id"))
    return model.model_validate(document)


class BaseRepository(BaseRepositoryProtocol[T], Generic[T]):
    domain_model: type[T]
    collection_name: ClassVar[str]

    def __init__(self, database: Database[MongoDocument]):
        self.database = database
        self.collection = self.database[self.collection_name]

    def _to_domain_entity(self, document: MongoDocument) -> T:
        return to_domain_entity(model=self.domain_model, document=document)

    @staticmethod
    def _to_database_entity(entity: T) -> MongoDocument:
        return entity.model_dump(exclude={"id"})

    def _paginate_cursor(
        self,
        pagination: Pagination,
        total: int,
        items: list[MongoDocument],
    ) -> PaginatedResponse[T]:
        entities = [self._to_domain_entity(document) for document in items]
        return PaginatedResponse(total=total, limit=pagination.limit, items=entities)

    def get_all(self, pagination: Pagination | None = None) -> PaginatedResponse[T]:
        pagination = pagination or Pagination()
        skip = (pagination.page - 1) * pagination.limit
        total = self.collection.count_documents({})
        cursor = self.collection.find({}).skip(skip).limit(pagination.limit)
        items = list(cursor)
        return self._paginate_cursor(pagination=pagination, total=total, items=items)

    def get_one(self, entity_id: EntityId, /) -> T | None:
        document = self.collection.find_one({"_id": ObjectId(entity_id)})
        return self._to_domain_entity(document) if document else None

    def create(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)
        result = self.collection.insert_one(db_entity)
        entity.id = EntityId(result.inserted_id)
        return entity

    def update(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)
        self.collection.replace_one({"_id": ObjectId(entity.id)}, db_entity)
        return entity

    def delete(self, entity_id: EntityId, /) -> None:
        self.collection.delete_one({"_id": ObjectId(entity_id)})
