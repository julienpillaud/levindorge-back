from app.domain.producers.entities import Producer
from app.domain.producers.repository import ProducerRepositoryProtocol
from app.infrastructure.repository.base import BaseRepository


class ProducerRepository(BaseRepository[Producer], ProducerRepositoryProtocol):
    domain_model = Producer
    collection_name = "producers"
