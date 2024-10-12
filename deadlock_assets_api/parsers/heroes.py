from deadlock_assets_api.models.hero import Hero
from deadlock_assets_api.models.v2.raw_hero import RawHero


def parse_heroes(data: dict) -> list[Hero]:
    hero_dicts = {
        k.removeprefix("hero_"): v
        for k, v in data.items()
        if k.startswith("hero_")
        and "base" not in k
        and "generic" not in k
        and "dummy" not in k
    }
    return [Hero(class_name=name, **v) for name, v in hero_dicts.items()]


def parse_heroes_v2(data: dict) -> list[RawHero]:
    hero_dicts = {
        k: v
        for k, v in data.items()
        if k.startswith("hero_")
        and "base" not in k
        and "generic" not in k
        and "dummy" not in k
    }
    return [RawHero(class_name=name, **v) for name, v in hero_dicts.items()]
