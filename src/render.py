from inspect import isclass
from typing import IO, Optional, Union

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class InputData(BaseModel):
    source: type[Union[BaseModel, BaseSettings]]


class SharedData(BaseModel):
    longest_name_length: int


class EnvItem(BaseModel):
    name: str
    comment: Optional[str] = None

    shared_data: SharedData

    def render(self) -> str:
        out = self.name + "=" + "example"
        if self.comment is not None:
            n_spaces = self.shared_data.longest_name_length - len(self.name)
            out += (n_spaces * " ") + "  # " + self.comment

        return out


def create_items(input_data: InputData, *, prefix="") -> list[EnvItem]:
    shared_data = SharedData(longest_name_length=0)

    def _inner(_input_data: InputData, _prefix=""):
        source = _input_data.source

        if env_prefix := source.model_config.get("env_prefix"):
            _prefix += env_prefix

        items = list[EnvItem]()

        for k, v in source.model_fields.items():
            name = _prefix + k

            shared_data.longest_name_length = max(len(name), shared_data.longest_name_length)

            if isclass(v.annotation) and issubclass(v.annotation, (BaseModel)):
                delimiter = source.model_config.get("env_nested_delimiter") or ""
                items += _inner(InputData(source=v.annotation), name + delimiter)
                continue

            item = EnvItem(name=name, shared_data=shared_data)

            item.comment = str(v.annotation)

            items.append(item)

        return items

    return _inner(input_data, prefix)


def create_example(input_data: InputData, file: IO):
    items = create_items(input_data)
    for item in items:
        print(item.render(), file=file)
