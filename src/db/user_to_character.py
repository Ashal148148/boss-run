from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class UserToCharacter(Base):
    __tablename__ = "UserToCharacter"

    user_id = Column(ForeignKey("User.id"), primary_key=True)
    character_id = Column(ForeignKey("Character.id"), primary_key=True)
