from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.config.database import Base

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(30))
    department = Column(String(150))
    year = Column(String(50))
    status = Column(String(30), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime

from app.config.database import Base


class RegistrationControl(Base):
    __tablename__ = "registration_controls"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(Integer, nullable=False, unique=True, index=True)

    is_open = Column(Boolean, default=False, nullable=False)

    requirements = Column(Text, nullable=True)

    opened_at = Column(DateTime, nullable=True)

    closed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
