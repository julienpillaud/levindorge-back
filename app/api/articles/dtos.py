from pydantic import BaseModel


class ArticleDTO(BaseModel):
    id: str
