from typing import Optional
from pydantic import BaseModel, EmailStr
class RegistrationCreate(BaseModel):
    event_id: Optional[int] = None
    name: str
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    year: Optional[str] = None
class RegistrationStatus(BaseModel):
    status: str
class RegistrationResponse(RegistrationCreate):
    id: int
    status: str
    class Config:
        from_attributes = True
