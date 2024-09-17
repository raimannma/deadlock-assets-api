from deadlock_assets_api.models.hero import Hero


def parse_heroes(data: dict) -> list[Hero]:
    hero_dicts = {
        k.removeprefix("hero_"): v
        for k, v in data.items()
        if k.startswith("hero_") and k != "hero_base"
    }
    return [Hero(class_name=name, **v) for name, v in hero_dicts.items()]
