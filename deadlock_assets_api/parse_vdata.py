import json

from kv3parser import KV3Parser

from deadlock_assets_api.models.hero import Hero


def parse_heroes(data: dict) -> list[Hero]:
    hero_dicts = {
        k.removeprefix("hero_"): v
        for k, v in data.items()
        if k.startswith("hero_") and k != "hero_base"
    }
    return [Hero(name=k, **v) for k, v in hero_dicts.items()]


VDATA_FILES = [
    (parse_heroes, "vdata/heroes.vdata", "res/heroes.json"),
]

if __name__ == "__main__":
    for parse_func, file_path, out_path in VDATA_FILES:
        with open(file_path, "r") as f:
            data = KV3Parser(f.read()).parse()
        data = parse_func(data)
        with open(out_path, "w") as f:
            if isinstance(data, list):
                json.dump([d.model_dump() for d in data], f, indent=4)
            if isinstance(data, dict):
                json.dump(data, f, indent=4)
