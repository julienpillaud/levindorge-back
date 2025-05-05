from typing import Any

from bson import ObjectId
from pymongo.collection import Collection

from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.entities import EntityId
from app.domain.producers.entities import Producer
from app.infrastructure.repository.base import MongoDocument

from .base import MongoBaseFactory
from .categories import CategoryFactory
from .producers import ProducerFactory


class ArticleFactory(MongoBaseFactory[Article]):
    def __init__(
        self,
        collection: Collection[MongoDocument],
        category_factory: CategoryFactory,
        producer_factory: ProducerFactory,
    ):
        super().__init__(collection)
        self.category_factory = category_factory
        self.producer_factory = producer_factory

    def _build_entity(self, **kwargs: Any) -> Article:
        category = self.category_factory.create_one()
        producer = self.producer_factory.create_one()

        return Article(
            id=EntityId(""),
            name=kwargs.get("name", self.faker.name()),
            category=Category.model_validate(category.model_dump()),
            producer=Producer.model_validate(producer.model_dump()),
        )

    def _to_database_entity(self, entity: Article, /) -> MongoDocument:
        return {
            "name": entity.name,
            "category_id": ObjectId(entity.category.id),
            "producer_id": ObjectId(entity.producer.id),
        }
