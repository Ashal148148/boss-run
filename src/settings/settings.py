from pydantic import BaseModel
from pydantic_settings import BaseSettings

class DBSettings(BaseModel):
    ign_max_len: int = 12
    ign_min_len: int = 4
    general_string_length: int = 50


class Settings(BaseSettings):
    db: DBSettings

    class Config:
        env_nested_delimiter = '__'
        env_file = '.env'
        