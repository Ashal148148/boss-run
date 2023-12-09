import os
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists
from sqlalchemy.exc import OperationalError
import logging

from .base import Base
from ..settings import settings

logger = logging.getLogger(__name__)

logger.info('attempting to connect to the data base')
try:
    engine = create_engine(str(settings.db.connection_string), echo=False)
    engine.connect()
except OperationalError:
    logger.error('failed to connect to the db')
    raise

if not database_exists(str(settings.db.connection_string)):
    Base.metadata.create_all(engine)
