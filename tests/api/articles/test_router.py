from fastapi import status
from fastapi.testclient import TestClient

from app.domain.entities import DEFAULT_PAGINATION_LIMIT

from ...fixtures.factories.articles import ArticleFactory
from ...fixtures.factories.categories import CategoryFactory
from ...fixtures.factories.producers import ProducerFactory


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


def test_get_article_not_found(client: TestClient):
    # Act
    article_id = "112233445566778899aabbcc"
    response = client.get(f"/articles/{article_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result["detail"] == f"Article '{article_id}' not found."


def test_create_article(
    category_factory: CategoryFactory,
    producer_factory: ProducerFactory,
    client: TestClient,
):
    # Arrange
    article_name = "Test Article"
    category = category_factory.create_one()
    producer = producer_factory.create_one()
    data = {
        "name": article_name,
        "category_id": str(category.id),
        "producer_id": str(producer.id),
    }

    # Act
    response = client.post("/articles", json=data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result["id"] is not None
    assert result["name"] == article_name
    assert result["category"] == category.model_dump()
    assert result["producer"] == producer.model_dump()


def test_create_article_invalid_category(
    producer_factory: ProducerFactory,
    client: TestClient,
):
    # Arrange
    article_name = "Test Article"
    category_id = "112233445566778899aabbcc"
    producer = producer_factory.create_one()
    data = {
        "name": article_name,
        "category_id": category_id,
        "producer_id": str(producer.id),
    }

    # Act
    response = client.post("/articles", json=data)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    result = response.json()
    assert result["detail"] == [
        {
            "type": "value_error",
            "loc": ["body", "category_id"],
            "msg": f"category_id '{category_id}' not found.",
            "input": category_id,
        }
    ]


def test_create_article_invalid_producer(
    category_factory: CategoryFactory,
    client: TestClient,
):
    # Arrange
    article_name = "Test Article"
    producer_id = "112233445566778899aabbcc"
    category = category_factory.create_one()
    data = {
        "name": article_name,
        "category_id": str(category.id),
        "producer_id": producer_id,
    }

    # Act
    response = client.post("/articles", json=data)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    result = response.json()
    assert result["detail"] == [
        {
            "type": "value_error",
            "loc": ["body", "producer_id"],
            "msg": f"producer_id '{producer_id}' not found.",
            "input": producer_id,
        }
    ]


def test_update_article(
    article_factory: ArticleFactory,
    client: TestClient,
):
    # Arrange
    article = article_factory.create_one()
    data = {"name": "Updated Name"}

    # Act
    response = client.patch(f"/articles/{article.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(article.id)
    assert result["name"] == data["name"]
    assert result["category"] == article.category.model_dump()
    assert result["producer"] == article.producer.model_dump()


def test_update_article_category(
    category_factory: CategoryFactory,
    article_factory: ArticleFactory,
    client: TestClient,
):
    # Arrange
    category = category_factory.create_one()
    article = article_factory.create_one()
    data = {"category_id": str(category.id)}

    # Act
    response = client.patch(f"/articles/{article.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(article.id)
    assert result["name"] == article.name
    assert result["category"] == category.model_dump()
    assert result["producer"] == article.producer.model_dump()


def test_update_article_producer(
    producer_factory: ProducerFactory,
    article_factory: ArticleFactory,
    client: TestClient,
):
    # Arrange
    producer = producer_factory.create_one()
    article = article_factory.create_one()
    data = {"producer_id": str(producer.id)}

    # Act
    response = client.patch(f"/articles/{article.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(article.id)
    assert result["name"] == article.name
    assert result["category"] == article.category.model_dump()
    assert result["producer"] == producer.model_dump()


def test_update_article_not_found(client: TestClient):
    # Arrange
    article_id = "112233445566778899aabbcc"
    data = {"name": "Updated Name"}

    # Act
    response = client.patch(f"/articles/{article_id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result["detail"] == f"Article '{article_id}' not found."


def test_update_article_invalid_category(
    article_factory: ArticleFactory,
    client: TestClient,
):
    # Arrange
    category_id = "112233445566778899aabbcc"
    article = article_factory.create_one()
    data = {"category_id": category_id}

    # Act
    response = client.patch(f"/articles/{article.id}", json=data)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    result = response.json()
    assert result["detail"] == [
        {
            "type": "value_error",
            "loc": ["body", "category_id"],
            "msg": f"category_id '{category_id}' not found.",
            "input": category_id,
        }
    ]


def test_delete_article(
    article_factory: ArticleFactory,
    client: TestClient,
):
    # Arrange
    article = article_factory.create_one()

    # Act
    response = client.delete(f"/articles/{article.id}")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get(f"/articles/{article.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_article_not_found(client: TestClient):
    # Arrange
    article_id = "112233445566778899aabbcc"

    # Act
    response = client.delete(f"/articles/{article_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result["detail"] == f"Article '{article_id}' not found."
