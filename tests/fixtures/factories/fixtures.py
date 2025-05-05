import pytest
from pymongo.synchronous.database import Database

from app.infrastructure.repository.base import MongoDocument
from tests.fixtures.factories.articles import ArticleFactory
from tests.fixtures.factories.categories import CategoryFactory
from tests.fixtures.factories.producers import ProducerFactory


@pytest.fixture(scope="session")
def category_factory(database: Database[MongoDocument]) -> CategoryFactory:
    return CategoryFactory(collection=database["categories"])


@pytest.fixture(scope="session")
def producer_factory(database: Database[MongoDocument]) -> ProducerFactory:
    return ProducerFactory(collection=database["producers"])


@pytest.fixture(scope="session")
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
