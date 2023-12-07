from fastapi import Request
from src.crud import user_crud
from sqlalchemy.orm import Session

from ..crud import ResouceNotFoundException

def accept_user(request: Request, session: Session):
    try:
        a = user_crud.read(session, request.session["id"])
        # print("sassssssssssssssssssssssssss", a.id) 
        id = a.id
    except ResouceNotFoundException:
        b = user_crud.create(session=session, session_id=request.session["id"])
        # print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", b.id)
        id = b.id
    return id
