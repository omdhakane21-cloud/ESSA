from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.config.database import Base

class GalleryImage(Base):
    __tablename__ = "gallery_images"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    image = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
