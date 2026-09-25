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

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class RegistrationCreate(BaseModel):

    event_id: int

    name: str

    email: EmailStr

    phone: str

    roll_number: str

    department: str

    year: str


class RegistrationResponse(BaseModel):

    id: int

    event_id: int

    name: str

    email: str

    phone: str

    roll_number: str

    department: str

    year: str

    status: str

    created_at: datetime

    class Config:
        from_attributes = True


class RegistrationStatus(BaseModel):

    status: str
