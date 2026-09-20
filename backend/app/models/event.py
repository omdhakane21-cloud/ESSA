from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.config.database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(DateTime)
    location = Column(String(200))
    image = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
