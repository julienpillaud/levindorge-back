from typing import Protocol

from cleanstack.domain import UnitOfWorkProtocol

from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.categories.repository import CategoryRepositoryProtocol
from app.domain.producers.repository import ProducerRepositoryProtocol


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def category_repository(self) -> CategoryRepositoryProtocol: ...
    @property
    def producer_repository(self) -> ProducerRepositoryProtocol: ...
    @property
    def article_repository(self) -> ArticleRepositoryProtocol: ...
