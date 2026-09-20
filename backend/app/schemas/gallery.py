from typing import Optional
from pydantic import BaseModel
class GalleryResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    image: str
    class Config:
        from_attributes = True
