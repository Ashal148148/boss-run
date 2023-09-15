from sqlalchemy import Column, Integer, String

from src.settings import settings
from .base import Base


class Character(Base):
    __tablename__ = "Character"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ign = Column(String(settings.db.ign_max_len))
