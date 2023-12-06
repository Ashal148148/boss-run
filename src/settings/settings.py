from typing import Tuple, Type
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SecretsSettingsSource

from .secret_source import MyCustomSource
from .schemas import SqliteDsn

class TableSettings(BaseModel):
    ign_max_len: int = 12
    ign_min_len: int = 4
    general_string_length: int = 50
    uuid_length: int = 36


class DBSettings(BaseModel):
    tables: TableSettings
    connection_string: SqliteDsn | PostgresDsn


class Settings(BaseSettings):
    db: DBSettings

    class Config:
        env_nested_delimiter = '__'
        env_file = '.env'
        secrets_dir = 'secrets'

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls, secrets_nested_delimiter='__'), env_settings, dotenv_settings)
        
