import pytest
from pymongo.database import Database

from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.base import MongoDocument


@pytest.fixture
def article_repository(database: Database[MongoDocument]) -> ArticleRepository:
    return ArticleRepository(database=database)
