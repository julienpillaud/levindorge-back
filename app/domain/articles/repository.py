from app.domain.articles.entities import Article
from app.domain.repository import BaseRepositoryProtocol


class ArticleRepositoryProtocol(BaseRepositoryProtocol[Article]):
    pass
