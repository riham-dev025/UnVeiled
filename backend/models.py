#handles data validation
from pydantic import BaseModel
from typing import Optional

#updated this file so content and url are both optional
class ArticleRequest(BaseModel):
    content: Optional[str] = None
    url: Optional[str] = None