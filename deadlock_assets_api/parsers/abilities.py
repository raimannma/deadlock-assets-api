from deadlock_assets_api.models.ability import Ability


def parse_abilities(data: dict) -> list[Ability]:
    ability_dicts = {
        k: v
        for k, v in data.items()
        if k.startswith("citadel_")
        or k.startswith("upgrade_")
        or k.startswith("ability_")
    }
    return [Ability(name=k, **v) for k, v in ability_dicts.items()]
