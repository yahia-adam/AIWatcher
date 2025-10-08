# Définit le format JSON de l'API
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ArticleBase(BaseModel):
    title: str
    url: str
    source: str

class ArticleCreate(ArticleBase):
    raw_content: str
    author: List[str]

class ArticleResponse(ArticleBase):
    id: int
    published_date: datetime
    is_processed: bool
    reading_time: int
    
    class Config:
        from_attributes = True  # Pour SQLAlchemy