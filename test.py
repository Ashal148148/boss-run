from src.db import Base
from src.db.engine import engine

Base.metadata.create_all(engine)
