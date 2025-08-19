from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.entities import Pagination

from ...fixtures.factories.articles import ArticleFactory


def test_pagination_request_less_than_total(
    article_factory: ArticleFactory,
    article_repository: ArticleRepositoryProtocol,
) -> None:
    # Arrange
    total_number = 9
    request_number = 5
    pagination = Pagination(page=1, limit=request_number)
    article_factory.create_many(total_number)

    # Act
    response = article_repository.get_all(pagination=pagination)

    # Assert
    assert response.total == total_number
    assert response.limit == request_number
    assert len(response.items) == request_number


def test_pagination_request_more_than_total(
    article_factory: ArticleFactory,
    article_repository: ArticleRepositoryProtocol,
) -> None:
    # Arrange
    total_number = 9
    request_number = 5
    pagination = Pagination(page=2, limit=request_number)
    article_factory.create_many(total_number)

    # Act
    response = article_repository.get_all(pagination=pagination)

    # Assert
    assert response.total == total_number
    assert response.limit == request_number
    assert len(response.items) == total_number - request_number


def test_pagination_out_of_range(
    article_factory: ArticleFactory,
    article_repository: ArticleRepositoryProtocol,
) -> None:
    # Arrange
    total_number = 9
    request_number = 5
    pagination = Pagination(page=3, limit=request_number)
    article_factory.create_many(total_number)

    # Act
    response = article_repository.get_all(pagination=pagination)

    # Assert
    assert response.total == total_number
    assert response.limit == request_number
    assert len(response.items) == 0
