import json

from kv3parser import KV3Parser
from pydantic import BaseModel

from deadlock_assets_api.models.ability import Ability
from deadlock_assets_api.models.hero import Hero, HeroImages


def parse_heroes(data: dict) -> list[Hero]:
    hero_dicts = {
        k.removeprefix("hero_"): v
        for k, v in data.items()
        if k.startswith("hero_") and k != "hero_base"
    }
    images = [
        ("portrait", ""),
        ("card", "_card"),
        ("vertical", "_vertical"),
        ("mm", "_mm"),
        ("sm", "_sm"),
        ("gun", "_gun"),
    ]
    return [
        Hero(
            name=name,
            images=HeroImages(
                **{
                    img_name: f"images/heroes/{name}{postfix}_psd.png"
                    for (img_name, postfix) in images
                }
            ),
            **v,
        )
        for name, v in hero_dicts.items()
    ]


def parse_abilities(data: dict) -> list[Ability]:
    ability_dicts = {
        k.removeprefix("citadel_").removeprefix("upgrade_"): v
        for k, v in data.items()
        if k.startswith("citadel_") or k.startswith("upgrade_")
    }
    return [Ability(name=k, **v) for k, v in ability_dicts.items()]


VDATA_FILES = [
    (parse_heroes, "vdata/heroes.vdata", "res/heroes.json"),
    (parse_abilities, "vdata/abilities.vdata", "res/abilities.json"),
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
