from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from src.settings import settings
from .base import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(settings.db.tables.uuid_length))
    last_seen = Column(DateTime, default=func.now())
    
    equipment = relationship("Equipment", back_populates="user")

    
