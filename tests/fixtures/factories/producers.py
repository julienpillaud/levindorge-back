from typing import Any

from app.domain.producers.entities import Producer

from .base import MongoBaseFactory


class ProducerFactory(MongoBaseFactory[Producer]):
    def _build_entity(self, **kwargs: Any) -> Producer:
        return Producer(
            id=None,
            name=kwargs.get("name", self.faker.name()),
        )
