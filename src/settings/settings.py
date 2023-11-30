from pathlib import Path
from typing import Any, Tuple, Type
import warnings
from pydantic import BaseModel, PostgresDsn
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SecretsSettingsSource
from pydantic_settings.sources import SettingsError

class TableSettings(BaseModel):
    ign_max_len: int = 12
    ign_min_len: int = 4
    general_string_length: int = 50


class DBSettings(BaseModel):
    tables: TableSettings
    connection_string: str | PostgresDsn


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
        return (MyCustomSource(settings_cls),)
        
class MyCustomSource(SecretsSettingsSource):
    def __call__(self) -> dict[str, Any]:
        """
        Build fields from "secrets" files.
        """
        secrets: dict[str, str | None] = {}

        if self.secrets_dir is None:
            return secrets

        self.secrets_path = Path(self.secrets_dir).expanduser()

        if not self.secrets_path.exists():
            warnings.warn(f'directory "{self.secrets_path}" does not exist')
            return secrets

        if not self.secrets_path.is_dir():
            raise SettingsError(f'secrets_dir must reference a directory')

        data: dict[str, Any] = {}

        print(self.settings_cls.model_fields['db'].metadata)

        for field_name, field in self.settings_cls.model_fields.items():
            try:
                field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            except Exception as e:
                raise SettingsError(
                    f'error getting value for field "{field_name}" from source "{self.__class__.__name__}"'
                ) from e

            try:
                field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)
            except ValueError as e:
                raise SettingsError(
                    f'error parsing value for field "{field_name}" from source "{self.__class__.__name__}"'
                ) from e            
            print(field_key)
            print(field_value)

        return data
