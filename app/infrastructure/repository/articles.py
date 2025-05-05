from typing import Any

from bson import ObjectId

from app.domain.articles.entities import Article
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.categories.entities import Category
from app.domain.entities import EntityId, PaginatedResponse, Pagination
from app.domain.producers.entities import Producer
from app.infrastructure.repository.base import (
    BaseRepository,
    MongoDocument,
    to_domain_entity,
)


class ArticleRepository(BaseRepository[Article], ArticleRepositoryProtocol):
    domain_model = Article
    collection_name = "articles"

    def _to_domain_entity(self, document: MongoDocument) -> Article:
        return Article(
            id=EntityId(str(document["_id"])),
            name=document["name"],
            category=to_domain_entity(model=Category, document=document["category"]),
            producer=to_domain_entity(model=Producer, document=document["producer"]),
        )

    def get_all(
        self, pagination: Pagination | None = None
    ) -> PaginatedResponse[Article]:
        pagination = pagination or Pagination()
        skip = (pagination.page - 1) * pagination.limit

        pipeline = [
            *self._aggregation_pipeline(),
            {"$skip": skip},
            {"$limit": pagination.limit},
        ]

        items = list(self.collection.aggregate(pipeline))
        total = self.collection.count_documents({})

        return self._paginate_cursor(pagination=pagination, total=total, items=items)

    def get_one(self, entity_id: EntityId, /) -> Article | None:
        pipeline = [
            {"$match": {"_id": ObjectId(entity_id)}},
            *self._aggregation_pipeline(),
        ]
        document = next(self.collection.aggregate(pipeline), None)
        return self._to_domain_entity(document) if document else None

    @staticmethod
    def _aggregation_pipeline() -> list[dict[str, Any]]:
        return [
            {
                "$lookup": {
                    "from": "categories",
                    "localField": "category_id",
                    "foreignField": "_id",
                    "as": "category",
                }
            },
            {"$unwind": "$category"},
            {
                "$lookup": {
                    "from": "producers",
                    "localField": "producer_id",
                    "foreignField": "_id",
                    "as": "producer",
                }
            },
            {"$unwind": "$producer"},
        ]
