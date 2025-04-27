from typing import Protocol

from app.domain.articles.repository import ArticleRepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def article_repository(self) -> ArticleRepositoryProtocol: ...
