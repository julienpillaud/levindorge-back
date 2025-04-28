from app.domain.articles.entities import Article
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.infrastructure.repository.base import BaseRepository


class ArticleRepository(BaseRepository[Article], ArticleRepositoryProtocol):
    domain_model = Article
    collection_name = "articles"
