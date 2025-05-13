from typing import Any

from app.domain.articles.entities import Article, ArticleCreate, ArticleUpdate
from app.domain.categories.entities import Category
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse, Pagination
from app.domain.exceptions import NotFoundError, UnprocessableContentError
from app.domain.producers.entities import Producer


def get_articles_command(
    context: ContextProtocol, pagination: Pagination
) -> PaginatedResponse[Article]:
    return context.article_repository.get_all(pagination=pagination)


def get_article_command(context: ContextProtocol, article_id: EntityId) -> Article:
    article = context.article_repository.get_one(article_id)
    if not article:
        raise NotFoundError(f"Article '{article_id}' not found.")

    return article


def create_article_command(context: ContextProtocol, data: ArticleCreate) -> Article:
    invalid_refs: list[tuple[str, Any]] = []
    category = _get_category(
        context=context,
        invalid_refs=invalid_refs,
        category_id=data.category_id,
    )
    producer = _get_producer(
        context=context,
        invalid_refs=invalid_refs,
        producer_id=data.producer_id,
    )
    if not category or not producer:
        raise UnprocessableContentError(invalid_refs)

    article = Article(
        id=None,
        name=data.name,
        category=category,
        producer=producer,
    )
    return context.article_repository.create(article)


def update_article_command(
    context: ContextProtocol, article_id: EntityId, data: ArticleUpdate
) -> Article:
    article = context.article_repository.get_one(article_id)
    if not article:
        raise NotFoundError(f"Article '{article_id}' not found.")

    invalid_refs: list[tuple[str, Any]] = []

    if data.category_id:
        category = _get_category(
            context=context,
            invalid_refs=invalid_refs,
            category_id=data.category_id,
        )
        if category:
            article.category = category

    if data.producer_id:
        producer = _get_producer(
            context=context,
            invalid_refs=invalid_refs,
            producer_id=data.producer_id,
        )
        if producer:
            article.producer = producer

    if invalid_refs:
        raise UnprocessableContentError(invalid_refs)

    for key, value in data.model_dump(
        exclude_none=True,
        exclude={"category_id", "producer_id"},
    ).items():
        setattr(article, key, value)

    return context.article_repository.update(article)


def delete_article_command(context: ContextProtocol, article_id: EntityId) -> None:
    article = context.article_repository.get_one(article_id)
    if not article:
        raise NotFoundError(f"Article '{article_id}' not found.")

    context.article_repository.delete(article)


def _get_category(
    context: ContextProtocol,
    invalid_refs: list[tuple[str, Any]],
    category_id: EntityId,
) -> Category | None:
    category = context.category_repository.get_one(category_id)
    if not category:
        invalid_refs.append(("category_id", category_id))
        return None

    return category


def _get_producer(
    context: ContextProtocol,
    invalid_refs: list[tuple[str, Any]],
    producer_id: EntityId,
) -> Producer | None:
    producer = context.producer_repository.get_one(producer_id)
    if not producer:
        invalid_refs.append(("producer_id", producer_id))
        return None

    return producer
