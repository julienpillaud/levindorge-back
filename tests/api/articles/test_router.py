from fastapi import status
from fastapi.testclient import TestClient

from app.domain.entities import DEFAULT_PAGINATION_LIMIT

from ...fixtures.factories.articles import ArticleFactory


def test_get_articles(article_factory: ArticleFactory, client: TestClient):
    # Arrange
    number_of_articles = 3
    article_factory.create_many(number_of_articles)

    # Act
    response = client.get("/articles")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == number_of_articles
    assert result["limit"] == DEFAULT_PAGINATION_LIMIT
    assert len(result["items"]) == number_of_articles


def test_get_article(article_factory: ArticleFactory, client: TestClient):
    # Arrange
    article = article_factory.create_one()

    # Act
    response = client.get(f"/articles/{article.id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(article.id)
    assert result["name"] == article.name
    assert result["category"] == article.category.model_dump()
    assert result["producer"] == article.producer.model_dump()
