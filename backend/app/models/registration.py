from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.config.database import Base


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(Integer, nullable=False)

    name = Column(String(150), nullable=False)

    email = Column(String(150), nullable=False)

    phone = Column(String(30), nullable=False)

    roll_number = Column(String(50), nullable=False)

    department = Column(String(150), nullable=False)

    year = Column(String(50), nullable=False)

    status = Column(String(30), default="pending")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class RegistrationControl(Base):
    __tablename__ = "registration_controls"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(Integer, nullable=False, unique=True)

    is_open = Column(Boolean, default=False, nullable=False)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )
