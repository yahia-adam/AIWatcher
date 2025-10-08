from pydantic import BaseModel

class SummaryBase(BaseModel):
    short_summary: str
    medium_summary: str

class SummaryResponse(SummaryBase):
    id: int
    article_id: int
    confidence_score: float
    
    class Config:
        from_attributes = True