from app.domain.articles.entities import Article
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse, Pagination


def get_articles_command(
    context: ContextProtocol, pagination: Pagination
) -> PaginatedResponse[Article]:
    return context.article_repository.get_all(pagination=pagination)
