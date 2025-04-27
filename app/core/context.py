from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import Settings
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.domain import TransactionalContextProtocol
from app.infrastructure.repository.articles import ArticleRepository


class Context(TransactionalContextProtocol):
    def __init__(self, settings: Settings):
        self.client: MongoClient[dict[str, Any]] = MongoClient(settings.MONGO_URI)
        self.database: Database[dict[str, Any]] = self.client[settings.MONGO_DATABASE]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    @property
    def article_repository(self) -> ArticleRepositoryProtocol:
        return ArticleRepository(database=self.database)
