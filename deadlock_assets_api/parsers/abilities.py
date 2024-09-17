from deadlock_assets_api.models.component import Component


def parse_abilities(data: dict) -> list[Component]:
    ability_dicts = {
        k: v
        for k, v in data.items()
        if k.startswith("citadel_")
        or k.startswith("upgrade_")
        or k.startswith("ability_")
    }
    return [Component(name=k, **v) for k, v in ability_dicts.items()]
