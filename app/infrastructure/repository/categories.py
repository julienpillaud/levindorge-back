from app.domain.categories.entities import Category
from app.domain.categories.repository import CategoryRepositoryProtocol
from app.infrastructure.repository.base import BaseRepository


class CategoryRepository(BaseRepository[Category], CategoryRepositoryProtocol):
    domain_model = Category
    collection_name = "categories"
