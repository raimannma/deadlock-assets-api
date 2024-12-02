import json
import os
import re

from deadlock_assets_api.models.languages import Language


def get_translation(key: str, language: Language, return_none: bool = False) -> str:
    for file in [
        f"res/localization/citadel_heroes_{language.value}.json"
        f"res/localization/citadel_gc_{language.value}.json",
        "res/localization/citadel_heroes_english.json",
        "res/localization/citadel_gc_english.json",
    ]:
        if not os.path.exists(file):
            continue
        with open(file) as f:
            language_data = json.load(f)["lang"]["Tokens"]
        name = language_data.get(key, None)
        if name is None:
            continue
        return name
    return key if not return_none else None


def prettify_snake_case(snake_str: str) -> str:
    return " ".join(
        re.sub(r"([a-zA-Z])(\d)", r"\1 \2", w.capitalize()) for w in snake_str.split("_")
    )


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def is_int(element: any) -> bool:
    if element is None:
        return False
    try:
        int(element)
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
