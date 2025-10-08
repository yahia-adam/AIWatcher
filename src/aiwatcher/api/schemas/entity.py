from pydantic import BaseModel

class EntityBase(BaseModel):
    entity_text: str
    entity_type: str
    confidence: float

class EntityResponse(EntityBase):
    id: int
    article_id: int
    canonical_name: str
    
    class Config:
        from_attributes = True