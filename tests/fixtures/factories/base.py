from typing import Any, Generic, TypeVar

from faker import Faker
from pymongo.collection import Collection

from app.domain.entities import DomainModel, EntityId
from app.infrastructure.repository.base import MongoDocument

T = TypeVar("T", bound=DomainModel)
P = TypeVar("P")


class BaseFactory(Generic[T, P]):
    def __init__(self):
        self.faker = Faker()

    def create_one(self, **kwargs: Any) -> T:
        entity = self._build_entity(**kwargs)
        self._insert([entity])
        return entity

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        entities = [self._build_entity(**kwargs) for _ in range(count)]
        self._insert(entities)
        return entities

    def _build_entity(self, **kwargs: Any) -> T:
        """Build a domain entity with the given kwargs."""
        ...

    def _insert(self, entities: list[T]) -> None:
        """Insert the entities into the database."""
        ...

    def _to_database_entity(self, entity: T, /) -> P:
        """Convert the domain entity to a database-compatible format."""
        ...


class MongoBaseFactory(BaseFactory[T, MongoDocument]):
    def __init__(self, collection: Collection[MongoDocument]):
        super().__init__()
        self.collection = collection

    def _insert(self, entities: list[T]) -> None:
        for entity in entities:
            db_entity = self._to_database_entity(entity)
            result = self.collection.insert_one(db_entity)
            entity.id = EntityId(str(result.inserted_id))

    def _to_database_entity(self, entity: T, /) -> MongoDocument:
        return entity.model_dump(exclude={"id"})
