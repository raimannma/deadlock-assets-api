from deadlock_assets_api.models.item import Item


def parse_items(data: dict) -> list[Item]:
    ability_dicts = {
        k: v
        for k, v in data.items()
        if k.startswith("citadel_")
        or k.startswith("upgrade_")
        or k.startswith("ability_")
    }
    return [Item(class_name=k, **v) for k, v in ability_dicts.items()]
