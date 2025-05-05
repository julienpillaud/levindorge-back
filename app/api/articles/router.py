from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_domain
from app.domain.articles.entities import Article
from app.domain.domain import Domain
from app.domain.entities import EntityId, PaginatedResponse, Pagination

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=PaginatedResponse[Article])
def get_articles(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Query()],
):
    return domain.get_articles(pagination=pagination)


@router.get("/{article_id}", response_model=Article)
def get_article(
    domain: Annotated[Domain, Depends(get_domain)],
    article_id: EntityId,
):
    return domain.get_article(article_id=article_id)
