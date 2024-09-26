from deadlock_assets_api.models.hero import Hero


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
