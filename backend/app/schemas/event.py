from datetime import datetime
from typing import Optional
from pydantic import BaseModel
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
class EventResponse(EventCreate):
    id: int
    image: Optional[str] = None
    class Config:
        from_attributes = True
