import os
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists

from .base import Base
from ..settings import settings


engine = create_engine(str(settings.db.connection_string), echo=True)

if not database_exists(str(settings.db.connection_string)):
    Base.metadata.create_all(engine)
