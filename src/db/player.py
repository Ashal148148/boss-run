from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import mapped_column, relationship

from src.settings import settings
from .base import Base


class Player(Base):
    __tablename__ = "Player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(Integer)
    int_goal = Column(Integer)
    bonus_HP = Column(Integer)
    bonus_mana = Column(Integer)
    INT = Column(Integer)
    maple_warrior_precent = Column(Integer)
    fresh_AP = Column(Integer)
    washes = Column(Integer)
    is_adding_int = Column(Boolean)
    stale_ap = Column(Integer)
    name = Column(String(settings.db.tables.ign_max_len))
    job = Column(String(settings.db.tables.ign_max_len))
    main_stat = Column(Integer)
    is_adding_fresh_ap_into_hp = Column(Boolean)
    mp_washes = Column(Integer)
    fresh_ap_into_hp_total = Column(Integer)

    user_id = mapped_column(ForeignKey('User.id'), unique=True, nullable=False)
    user = relationship("User")
