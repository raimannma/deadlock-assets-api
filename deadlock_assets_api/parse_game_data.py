import json
import os

import vdf
from kv3parser import KV3Parser
from pydantic import BaseModel

from deadlock_assets_api.parsers.generic_data import parse_generic_data
from deadlock_assets_api.parsers.heroes import parse_heroes
from deadlock_assets_api.parsers.items import parse_items

VDATA_FILES = [
    (parse_generic_data, "vdata/generic_data.vdata", "res/generic_data.json"),
    (parse_heroes, "vdata/heroes.vdata", "res/heroes.json"),
    (parse_items, "vdata/abilities.vdata", "res/items.json"),
]


def parse_vdata():
    for parse_func, file_path, out_path in VDATA_FILES:
        with open(file_path) as f:
            data = KV3Parser(f.read()).parse()
        data = parse_func(data)
        if isinstance(data, list):
            data = [
                (
                    d.model_dump(exclude={"name"})
                    if isinstance(d, BaseModel)
                    else d.__dict__
                )
                for d in data
            ]
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude={"name"})
        with open(out_path, "w") as f:
            json.dump(data, f, indent=4)


def parse_vdf():
    for root, _, files in os.walk("localization"):
        for file in files:
            if not file.endswith(".txt"):
                continue
            file = os.path.join(root, file)
            # print(f"Reading {file}")
            with open(file, encoding="utf8", errors="ignore") as f:
                data = vdf.loads(f.read().replace("\ufeff", ""))
            out_file = os.path.join("res", file.replace(".txt", ".json"))
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            with open(out_file, "w") as f:
                json.dump(data, f, indent=4)


if __name__ == "__main__":
    parse_vdata()
    parse_vdf()
