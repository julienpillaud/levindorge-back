import pytest
from pymongo.synchronous.database import Database

from app.infrastructure.repository.base import MongoDocument

from .articles import ArticleFactory
from .categories import CategoryFactory
from .producers import ProducerFactory


@pytest.fixture
def category_factory(database: Database[MongoDocument]) -> CategoryFactory:
    return CategoryFactory(collection=database["categories"])


@pytest.fixture
def producer_factory(database: Database[MongoDocument]) -> ProducerFactory:
    return ProducerFactory(collection=database["producers"])


@pytest.fixture
def article_factory(
    database: Database[MongoDocument],
    category_factory: CategoryFactory,
    producer_factory: ProducerFactory,
) -> ArticleFactory:
    return ArticleFactory(
        collection=database["articles"],
        category_factory=category_factory,
        producer_factory=producer_factory,
    )
