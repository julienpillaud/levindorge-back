from typing import Any

from app.domain.categories.entities import Category
from app.domain.entities import EntityId

from .base import MongoBaseFactory


class CategoryFactory(MongoBaseFactory[Category]):
    def _build_entity(self, **kwargs: Any) -> Category:
        return Category(
            id=EntityId(""),
            name=kwargs.get("name", self.faker.name()),
        )
