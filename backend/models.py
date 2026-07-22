#handles data validation
from pydantic import BaseModel


class ArticleRequest(BaseModel):
    content: str