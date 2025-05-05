from typing import Any

from app.domain.entities import EntityId
from app.domain.producers.entities import Producer

from .base import MongoBaseFactory


class ProducerFactory(MongoBaseFactory[Producer]):
    def _build_entity(self, **kwargs: Any) -> Producer:
        return Producer(
            id=EntityId(""),
            name=kwargs.get("name", self.faker.name()),
        )
