from typing import Optional
from pydantic import BaseModel, EmailStr
class MessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
class MessageResponse(MessageCreate):
    id: int
    is_read: int
    class Config:
        from_attributes = True
