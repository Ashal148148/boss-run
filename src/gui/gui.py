from typing import Annotated
from fastapi import Cookie, Request
from nicegui import app, ui


@ui.page('/')
def root(request: Request) -> None:
    ui.label('hello world, how are you today')
    print(request.session["id"])
