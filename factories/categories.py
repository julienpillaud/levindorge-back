from typing import Any

from cleanstack.factories.mongo import MongoBaseFactory
from cleanstack.infrastructure.mongo.entities import MongoDocument
from polyfactory.factories.pydantic_factory import ModelFactory
from pymongo.collection import Collection

from app.domain.categories.entities import Category


class CategoryEntityFactory(ModelFactory[Category]): ...


class CategoryFactory(MongoBaseFactory[Category]):
    def __init__(self, collection: Collection[MongoDocument]) -> None:
        super().__init__(collection=collection)

    def _build_entity(self, **kwargs: Any) -> Category:
        return CategoryEntityFactory.build(**kwargs)
