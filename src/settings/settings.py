from pydantic import BaseModel
from pydantic_settings import BaseSettings

class DBSettings(BaseSettings):
    ign_max_len: int = 12
    ign_min_len: int = 4


class Settings(BaseSettings):
    db: DBSettings = DBSettings()