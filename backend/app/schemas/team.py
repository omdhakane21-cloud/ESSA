from typing import Optional
from pydantic import BaseModel
class TeamCreate(BaseModel):
    name: str
    role: str
    department: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    display_order: int = 0
    active: int = 1
class TeamResponse(TeamCreate):
    id: int
    photo: Optional[str] = None
    class Config:
        from_attributes = True
