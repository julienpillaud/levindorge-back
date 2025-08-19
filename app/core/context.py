from collections.abc import Iterator
from contextlib import contextmanager

from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import Settings
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.categories.repository import CategoryRepositoryProtocol
from app.domain.context import ContextProtocol
from app.domain.producers.repository import ProducerRepositoryProtocol
from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.base import MongoDocument
from app.infrastructure.repository.categories import CategoryRepository
from app.infrastructure.repository.producers import ProducerRepository


class Context(ContextProtocol):
    def __init__(self, settings: Settings):
        self.client: MongoClient[MongoDocument] = MongoClient(settings.MONGO_URI)
        self.database: Database[MongoDocument] = self.client[settings.MONGO_DATABASE]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    @property
    def category_repository(self) -> CategoryRepositoryProtocol:
        return CategoryRepository(database=self.database)

    @property
    def producer_repository(self) -> ProducerRepositoryProtocol:
        return ProducerRepository(database=self.database)

    @property
    def article_repository(self) -> ArticleRepositoryProtocol:
        return ArticleRepository(database=self.database)
