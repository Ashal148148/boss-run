from typing import List, Tuple
from uuid import UUID
from pydantic import PositiveInt
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import ResourceClosedError

from .error import ResourceNotFoundException
from .base import CRUDBase
from .user import user_crud
from ..db.player import Player
from ..wash_calculator import Player as PlayerSchema


class PlayerCRUD(CRUDBase):
    def read(self, session: Session, id: PositiveInt):
        try:
            r, = session.execute(select(Player).where(Player.id == id)).all()[0]
        except IndexError:
            raise ResourceNotFoundException()
        return r
    
    def read_by_session_id(self, session: Session, session_id: UUID) -> List[Tuple[Player,]]:
        user = user_crud.read(session=session, session_id=session_id)
        r, = session.execute(select(Player).where(Player.user_id == user.id)).all()
        return r
    
    def read_by_user_id(self, session: Session, user_id: int) -> Player:
        try:
            r, = session.execute(select(Player).where(Player.user_id == user_id)).all()[0]
        except IndexError:
            raise ResourceNotFoundException()
        return r
    
    def create(self, session: Session, user_id: int, player: PlayerSchema):
        r = Player(user_id = user_id, **player.dump_model())
        session.add(r)
        session.commit()
        return r
    
    def update(self, session: Session, user_id: int, player: PlayerSchema):
        self.read_by_user_id(session, user_id)
        r = session.execute(update(Player).where(Player.user_id == user_id), player.dump_model())
        session.commit()        
        return r
    
    def save(self, session: Session, user_id: int, player: PlayerSchema):
        try:
            return self.update(session, user_id, player)
        except ResourceNotFoundException:
            return self.create(session, user_id, player)
    
    def delete(self, session: Session, id: PositiveInt):
        r = session.execute(delete(Player).where(Player.id == id))
        session.commit()
        return r

player_crud = PlayerCRUD()