from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_domain
from app.domain.articles.entities import Article, ArticleCreate, ArticleUpdate
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
def get_article(domain: Annotated[Domain, Depends(get_domain)], article_id: EntityId):
    return domain.get_article(article_id=article_id)


@router.post("", response_model=Article, status_code=status.HTTP_201_CREATED)
def create_article(domain: Annotated[Domain, Depends(get_domain)], data: ArticleCreate):
    return domain.create_article(data=data)


@router.patch("/{article_id}", response_model=Article)
def update_article(
    domain: Annotated[Domain, Depends(get_domain)],
    article_id: EntityId,
    data: ArticleUpdate,
):
    return domain.update_article(article_id=article_id, data=data)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    domain: Annotated[Domain, Depends(get_domain)], article_id: EntityId
):
    domain.delete_article(article_id=article_id)
