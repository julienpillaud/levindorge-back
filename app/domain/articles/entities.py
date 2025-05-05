from app.domain.categories.entities import Category
from app.domain.entities import DomainModel
from app.domain.producers.entities import Producer


class Article(DomainModel):
    name: str

    category: Category
    producer: Producer
