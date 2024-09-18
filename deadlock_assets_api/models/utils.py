import os
import re
from functools import lru_cache

from pydantic import TypeAdapter

from deadlock_assets_api.models.generic_data import GenericData
from deadlock_assets_api.models.hero import Hero
from deadlock_assets_api.models.item import Item


def prettify_snake_case(snake_str: str) -> str:
    return " ".join(
        re.sub(r"([a-zA-Z])(\d)", r"\1 \2", w.capitalize())
        for w in snake_str.split("_")
    )


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def camel_to_snake(s):
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def strip_prefix(string: str, prefix: str) -> str:
    prefix_index = string.find(prefix)
    if prefix_index != -1:
        return string[prefix_index + len(prefix) :]
    return string


@lru_cache
def load_heroes() -> list[Hero] | None:
    if not os.path.exists("res/heroes.json"):
        return None
    with open("res/heroes.json") as f:
        content = f.read()
    ta = TypeAdapter(list[Hero])
    return ta.validate_json(content)


@lru_cache
def load_items() -> list[Item] | None:
    if not os.path.exists("res/items.json"):
        return None
    with open("res/items.json") as f:
        content = f.read()
    ta = TypeAdapter(list[Item])
    return ta.validate_json(content)


@lru_cache
def load_generic_data() -> GenericData | None:
    if not os.path.exists("res/generic_data.json"):
        return None
    with open("res/generic_data.json") as f:
        return GenericData.model_validate_json(f.read())
