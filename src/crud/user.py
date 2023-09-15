from uuid import UUID
from pydantic import PositiveInt
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session
from .base import CRUDBase
from src.db import User

class UserCRUD(CRUDBase):
    def read(self, session: Session, session_id: PositiveInt):
        r = session.execute(select(User).where(User.session_id == session_id)).all()
        return r
    
    def create(self, session: Session, session_id: UUID):
        r = User(session_id=session_id)
        session.add(r)
        return r
    
    def delete(self, session: Session, id: PositiveInt):
        r = session.execute(delete(User).where(User.id == id))
        return r

user_crud = UserCRUD()