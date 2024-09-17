import json

from kv3parser import KV3Parser
from pydantic import BaseModel

from deadlock_assets_api.parsers.heroes import parse_heroes
from deadlock_assets_api.parsers.items import parse_items

VDATA_FILES = [
    (parse_heroes, "vdata/heroes.vdata", "res/heroes.json"),
    (parse_items, "vdata/abilities.vdata", "res/items.json"),
]

if __name__ == "__main__":
    for parse_func, file_path, out_path in VDATA_FILES:
        with open(file_path) as f:
            data = KV3Parser(f.read()).parse()
        data = parse_func(data)
        with open(out_path, "w") as f:
            if isinstance(data, list):
                json.dump(
                    [
                        d.model_dump() if isinstance(d, BaseModel) else d.__dict__
                        for d in data
                    ],
                    f,
                    indent=4,
                )
            if isinstance(data, dict):
                json.dump(data, f, indent=4)
