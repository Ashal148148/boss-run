from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from src.settings import settings
from .base import Base


class Equipment(Base):
    __tablename__ = "Equipment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(settings.db.tables.general_string_length))
    category = Column(String(settings.db.tables.general_string_length))
    level_requirement = Column(Integer)
    INT = Column(Integer)
    user_id = mapped_column(ForeignKey('User.id'))
    user = relationship("User", back_populates="equipment")
