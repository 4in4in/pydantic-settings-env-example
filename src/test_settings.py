from enum import Enum

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class NestedSettings(BaseModel):
    nested_1: str


class TestEnum(str, Enum):
    VALUE = "value"


class TestSettings(BaseSettings):
    integer: int
    optional_string: str | None = None

    nested: NestedSettings
    enum: TestEnum

    model_config = SettingsConfigDict(env_prefix="main_prefix_", env_nested_delimiter="___")
