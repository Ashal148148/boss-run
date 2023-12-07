from typing import List, Tuple
from uuid import UUID
from pydantic import PositiveInt
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session
from .base import CRUDBase
from .user import user_crud
from src.db import Equipment

class EquipmentCRUD(CRUDBase):
    def read(self, session: Session, id: PositiveInt):
        r = session.execute(select(Equipment).where(Equipment.id == id)).all()
        return r
    
    def read_by_session_id(self, session: Session, user_id: UUID) -> List[Tuple[Equipment,]]:        
        r = session.execute(select(Equipment).where(Equipment.user_id == user_id)).all()
        return r
    
    def create(self, session: Session, session_id: UUID, catagory: str, name: str, level: int, INT: int):
        user = user_crud.read(session=session, session_id=session_id)
        r = Equipment(catagory=catagory, name=name, level_requirement=level, INT=INT, user_id=user.id)
        session.add(r)
        session.commit()
        return r
    
    def delete(self, session: Session, id: PositiveInt):
        r = session.execute(delete(Equipment).where(Equipment.id == id))
        session.commit()
        return r

equipment_crud = EquipmentCRUD()