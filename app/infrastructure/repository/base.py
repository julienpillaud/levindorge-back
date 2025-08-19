from typing import Any, ClassVar, Generic, TypeVar

from cleanstack.entities import DomainModel, EntityId
from cleanstack.exceptions import NotFoundError
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.domain.entities import PaginatedResponse, Pagination
from app.domain.repository import BaseRepositoryProtocol

T = TypeVar("T", bound=DomainModel)


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

    def _get_entity_by_id(self, entity_id: EntityId, /) -> T | None:
        db_entity = self.collection.find_one({"_id": entity_id})
        return self._to_domain_entity(db_entity) if db_entity else None

    def _get_entity_by_id_or_raise(self, entity_id: EntityId) -> T:
        entity = self._get_entity_by_id(entity_id)
        if not entity:
            raise NotFoundError(f"Entity '{entity_id}' not found")
        return entity

    @staticmethod
    def _aggregation_pipeline() -> list[dict[str, Any]]:
        return []

    def get_all(self, pagination: Pagination | None = None) -> PaginatedResponse[T]:
        pagination = pagination or Pagination()
        skip = (pagination.page - 1) * pagination.limit

        pipeline = self._aggregation_pipeline()

        count_pipeline = [*pipeline, {"$count": "total"}]
        count_result = list(self.collection.aggregate(count_pipeline))
        total = count_result[0]["total"] if count_result else 0

        paginated_pipeline = [*pipeline, {"$skip": skip}, {"$limit": pagination.limit}]
        items_db = self.collection.aggregate(paginated_pipeline)
        items = [self._to_domain_entity(item) for item in items_db]

        return PaginatedResponse(total=total, limit=pagination.limit, items=items)

    def get_one(self, entity_id: EntityId, /) -> T | None:
        return self._get_entity_by_id(entity_id)

    def create(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)
        result = self.collection.insert_one(db_entity)
        return self._get_entity_by_id_or_raise(result.inserted_id)

    def update(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)
        self.collection.replace_one({"_id": entity.id}, db_entity)
        return self._get_entity_by_id_or_raise(entity.id)

    def delete(self, entity: T, /) -> None:
        self.collection.delete_one({"_id": entity.id})
