from cleanstack.entities import DomainModel, EntityId
from pydantic import BaseModel

from app.domain.categories.entities import Category
from app.domain.producers.entities import Producer


class ArticleCreate(BaseModel):
    name: str

    category_id: EntityId
    producer_id: EntityId


class ArticleUpdate(BaseModel):
    name: str | None = None

    category_id: EntityId | None = None
    producer_id: EntityId | None = None


class Article(DomainModel):
    name: str

    category: Category
    producer: Producer
