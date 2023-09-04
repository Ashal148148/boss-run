from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ign = Column(String(settings.db.ign_max_len))