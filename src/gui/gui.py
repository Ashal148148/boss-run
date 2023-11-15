from typing import Annotated
from fastapi import Cookie, Request, Depends
from nicegui import app, ui
from src.crud import user_crud
from sqlalchemy.orm import Session
from .dependencies import get_session
from .calculator import calculator


@ui.page('/asd')
def root(request: Request, session: Session = Depends(get_session)) -> None:
    ui.label('hello world, how are you today')
    print(request.session["id"])
    a = user_crud.read(session, request.session["id"])
    if not a:
        b = user_crud.create(session=session, session_id=request.session["id"])
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", b)
    print("sassssssssssssssssssssssssss", a.id)
    ui.button("Click me", on_click=lambda x: print(x))

