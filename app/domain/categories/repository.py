from app.domain.categories.entities import Category
from app.domain.repository import BaseRepositoryProtocol


class CategoryRepositoryProtocol(BaseRepositoryProtocol[Category]):
    pass
