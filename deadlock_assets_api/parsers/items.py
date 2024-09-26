from deadlock_assets_api.models.item import Item


def parse_items(data: dict) -> list[Item]:
    ability_dicts = {
        k: v
        for k, v in data.items()
        if "base" not in k
        and "dummy" not in k
        and ("generic" not in k or "citadel" in k)
        and isinstance(v, dict)
    }
    return [Item(class_name=k, **v) for k, v in ability_dicts.items()]
