from app.domain.articles.entities import Article
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse, Pagination
from app.domain.exceptions import NotFoundError


def get_articles_command(
    context: ContextProtocol, pagination: Pagination
) -> PaginatedResponse[Article]:
    return context.article_repository.get_all(pagination=pagination)


def get_article_command(context: ContextProtocol, article_id: EntityId) -> Article:
    article = context.article_repository.get_one(article_id)
    if not article:
        raise NotFoundError(f"Article '{article_id}' not found")

    return article
