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
