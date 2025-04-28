from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.articles.dtos import ArticleDTO
from app.api.dependencies import get_domain
from app.api.pagination.dtos import PaginatedResponseDTO, PaginationDTO
from app.domain.domain import Domain

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=PaginatedResponseDTO[ArticleDTO])
async def get_articles(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[PaginationDTO, Query()],
):
    return domain.get_articles(pagination=pagination.to_domain())
