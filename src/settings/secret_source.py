from collections import deque
from dataclasses import is_dataclass
import sys
from pathlib import Path
from typing import Any, Tuple, Type, TypeVar, Mapping, Union, Sequence, _GenericAlias
import types
from typing_extensions import get_origin, get_args
import warnings
from pydantic import BaseModel, PostgresDsn
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SecretsSettingsSource
from pydantic_settings.sources import SettingsError
from pydantic._internal._typing_extra import origin_is_union

KeyType = TypeVar('KeyType')

if sys.version_info < (3, 10):

    def origin_is_union(tp: type[Any] | None) -> bool:
        return tp is Union

    WithArgsTypes = (TypingGenericAlias,)

else:

    def origin_is_union(tp: type[Any] | None) -> bool:
        return tp is Union or tp is types.UnionType

    WithArgsTypes = _GenericAlias, types.GenericAlias, types.UnionType  # type: ignore[attr-defined]



class MyCustomSource(SecretsSettingsSource):

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        secrets_dir: str | Path | None = None,
        case_sensitive: bool | None = None,
        env_prefix: str | None = None,
        secrets_nested_delimiter: str | None = None,
        secrets_prefix: str | None = None,
    ) -> None:
        super().__init__(settings_cls, secrets_dir, case_sensitive, env_prefix)
        self.secrets_nested_delimiter = secrets_nested_delimiter
        self.secrets_prefix = secrets_prefix
        self.secrets_prefix_len = len(secrets_prefix) if secrets_prefix else 0

    def _field_is_complex(self, field: FieldInfo) -> tuple[bool, bool]:
        """
        Find out if a field is complex, and if so whether JSON errors should be ignored
        """
        if self.field_is_complex(field):
            allow_parse_failure = False
        elif origin_is_union(get_origin(field.annotation)) and self._union_is_complex(field.annotation, field.metadata):
            allow_parse_failure = True
        else:
            return False, False

        return True, allow_parse_failure
    
    def _union_is_complex(self, annotation: type[Any] | None, metadata: list[Any]) -> bool:
        return any(_annotation_is_complex(arg, metadata) for arg in get_args(annotation))
    
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

        for field_name, field in self.settings_cls.model_fields.items():
            try:
                field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            except Exception as e:
                raise SettingsError(
                    f'error getting value for field "{field_name}" from source "{self.__class__.__name__}"'
                ) from e

            try:
                field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)
                data[field_name] = field_value
            except ValueError as e:
                raise SettingsError(
                    f'error parsing value for field "{field_name}" from source "{self.__class__.__name__}"'
                ) from e            
            
        return data
    
    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        """
        Prepare value for the field.

        * Extract value for nested field.
        * Deserialize value to python object for complex field.

        Args:
            field: The field.
            field_name: The field name.

        Returns:
            A tuple contains prepared value for the field.

        Raises:
            ValuesError: When There is an error in deserializing value for complex field.
        """
        is_complex, allow_parse_failure = self._field_is_complex(field)
        if is_complex or value_is_complex:
            if value is None:
                # field is complex but no value found so far, try explode_env_vars
                secrets_in_dir = {}
                for file in self.secrets_path.iterdir():
                    secrets_in_dir[str(file.name)] = file.read_text()
                env_val_built = self.explode_env_vars(field_name, field, secrets_in_dir)
                if env_val_built:
                    return env_val_built
            else:
                # field is complex and there's a value, decode that as JSON, then add explode_env_vars
                try:
                    value = self.decode_complex_value(field_name, field, value)
                except ValueError as e:
                    if not allow_parse_failure:
                        raise e

                if isinstance(value, dict):
                    return deep_update(value, self.explode_env_vars(field_name, field, self.env_vars))
                else:
                    return value
        elif value is not None:
            # simplest case, field is not complex, we only need to add the value if it was found
            return value
        
    @staticmethod
    def next_field(field: FieldInfo | None, key: str) -> FieldInfo | None:
        """
        Find the field in a sub model by key(env name)

        By having the following models:

            ```py
            class SubSubModel(BaseSettings):
                dvals: Dict

            class SubModel(BaseSettings):
                vals: list[str]
                sub_sub_model: SubSubModel

            class Cfg(BaseSettings):
                sub_model: SubModel
            ```

        Then:
            next_field(sub_model, 'vals') Returns the `vals` field of `SubModel` class
            next_field(sub_model, 'sub_sub_model') Returns `sub_sub_model` field of `SubModel` class

        Args:
            field: The field.
            key: The key (env name).

        Returns:
            Field if it finds the next field otherwise `None`.
        """
        if not field or origin_is_union(get_origin(field.annotation)):
            # no support for Unions of complex BaseSettings fields
            return None
        elif field.annotation and hasattr(field.annotation, 'model_fields') and field.annotation.model_fields.get(key):
            return field.annotation.model_fields[key]

        return None
    
    def explode_env_vars(self, field_name: str, field: FieldInfo, env_vars: Mapping[str, str | None]) -> dict[str, Any]:
        """
        Process env_vars and extract the values of keys containing secrets_nested_delimiter into nested dictionaries.

        This is applied to a single field, hence filtering by env_var prefix.

        Args:
            field_name: The field name.
            field: The field.
            env_vars: Environment variables.

        Returns:
            A dictionaty contains extracted values from nested env values.
        """
        prefixes = [
            f'{env_name}{self.secrets_nested_delimiter}' for _, env_name, _ in self._extract_field_info(field, field_name)
        ]
        result: dict[str, Any] = {}
        for env_name, env_val in env_vars.items():
            if not any(env_name.startswith(prefix) for prefix in prefixes):
                continue
            # we remove the prefix before splitting in case the prefix has characters in common with the delimiter
            env_name_without_prefix = env_name[self.secrets_prefix_len :]
            _, *keys, last_key = env_name_without_prefix.split(self.secrets_nested_delimiter)
            env_var = result
            target_field: FieldInfo | None = field
            for key in keys:
                target_field = self.next_field(target_field, key)
                env_var = env_var.setdefault(key, {})

            # get proper field with last_key
            target_field = self.next_field(target_field, last_key)

            # check if env_val maps to a complex field and if so, parse the env_val
            if target_field and env_val:
                is_complex, allow_json_failure = self._field_is_complex(target_field)
                if is_complex:
                    try:
                        env_val = self.decode_complex_value(last_key, target_field, env_val)
                    except ValueError as e:
                        if not allow_json_failure:
                            raise e
            env_var[last_key] = env_val

        return result
    
def deep_update(mapping: dict[KeyType, Any], *updating_mappings: dict[KeyType, Any]) -> dict[KeyType, Any]:
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
                updated_mapping[k] = deep_update(updated_mapping[k], v)
            else:
                updated_mapping[k] = v
    return updated_mapping

def _annotation_is_complex(annotation: type[Any] | None, metadata: list[Any]) -> bool:
    if any(isinstance(md, Json) for md in metadata):  # type: ignore[misc]
        return False
    origin = get_origin(annotation)
    return (
        _annotation_is_complex_inner(annotation)
        or _annotation_is_complex_inner(origin)
        or hasattr(origin, '__pydantic_core_schema__')
        or hasattr(origin, '__get_pydantic_core_schema__')
    )



def _annotation_is_complex_inner(annotation: type[Any] | None) -> bool:
    if lenient_issubclass(annotation, (str, bytes)):
        return False

    return lenient_issubclass(annotation, (BaseModel, Mapping, Sequence, tuple, set, frozenset, deque)) or is_dataclass(
        annotation
    )

def lenient_issubclass(cls: Any, class_or_tuple: Any) -> bool:  # pragma: no cover
    try:
        return isinstance(cls, type) and issubclass(cls, class_or_tuple)
    except TypeError:
        if isinstance(cls, WithArgsTypes):
            return False
        raise  # pragma: no cover