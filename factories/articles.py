from typing import Any

from cleanstack.factories.mongo import MongoBaseFactory
from cleanstack.infrastructure.mongo.entities import MongoDocument
from polyfactory.factories.pydantic_factory import ModelFactory
from pymongo.collection import Collection

from app.domain.articles.entities import Article
from factories.categories import CategoryFactory
from factories.producers import ProducerFactory


class ArticleEntityFactory(ModelFactory[Article]): ...


class ArticleFactory(MongoBaseFactory[Article]):
    def __init__(self, collection: Collection[MongoDocument]) -> None:
        super().__init__(collection=collection)

    @property
    def producer_factory(self) -> ProducerFactory:
        return ProducerFactory(collection=self.collection)

    @property
    def category_factory(self) -> CategoryFactory:
        return CategoryFactory(collection=self.collection)

    def _build_entity(self, **kwargs: Any) -> Article:
        if "producer" not in kwargs:
            kwargs["producer"] = self.producer_factory.create_one()
        if "category" not in kwargs:
            kwargs["category"] = self.category_factory.create_one()
        return ArticleEntityFactory.build(**kwargs)
