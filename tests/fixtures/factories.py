import pytest
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from factories.categories import CategoryFactory


@pytest.fixture
def category_factory(database: Database[MongoDocument]) -> CategoryFactory:
    return CategoryFactory(collection=database["categories"])
