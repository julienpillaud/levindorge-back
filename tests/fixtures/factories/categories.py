from typing import Any

from app.domain.categories.entities import Category

from .base import MongoBaseFactory


class CategoryFactory(MongoBaseFactory[Category]):
    def _build_entity(self, **kwargs: Any) -> Category:
        return Category(
            id=None,
            name=kwargs.get("name", self.faker.name()),
        )
