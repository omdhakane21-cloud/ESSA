from sqlalchemy import Column, Integer, String, Text
from app.config.database import Base

class TeamMember(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    role = Column(String(100), nullable=False)
    department = Column(String(200))
    bio = Column(Text)
    phone = Column(String(30))
    email = Column(String(150))
    photo = Column(String(500))
    display_order = Column(Integer, default=0)
    active = Column(Integer, default=1)
