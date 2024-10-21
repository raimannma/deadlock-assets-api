import json
from pprint import pprint

from pydantic import ValidationError

from deadlock_assets_api import utils
from deadlock_assets_api.models.v2.raw_ability import RawAbilityV2
from deadlock_assets_api.models.v2.raw_upgrade import RawUpgradeV2
from deadlock_assets_api.models.v2.raw_weapon import RawWeaponV2


def test_parse():
    with open("res/raw_items.json") as f:
        raw_items = json.load(f)

    def parse(class_name, data) -> RawWeaponV2 | RawUpgradeV2 | RawAbilityV2:
        name = utils.strip_prefix(class_name, "citadel_").lower()
        first_word = name.split("_")[0]
        if first_word == "ability":
            return RawAbilityV2(class_name=class_name, **data)
        elif first_word == "upgrade":
            return RawUpgradeV2(class_name=class_name, **data)
        elif first_word == "weapon":
            return RawWeaponV2(class_name=class_name, **data)

        hero_list = [
            "astro",
            "atlas",
            "bebop",
            "bomber",
            "cadence",
            "chrono",
            "dynamo",
            "forge",
            "ghost",
            "gigawatt",
            "gunslinger",
            "haze",
            "hornet",
            "inferno",
            "kali",
            "kelvin",
            "krill",
            "lash",
            "mirage",
            "nano",
            "orion",
            "rutger",
            "shiv",
            "slork",
            "synth",
            "tengu",
            "thumper",
            "tokamak",
            "viscous",
            "warden",
            "wraith",
            "wrecker",
            "yakuza",
            "yamato",
        ]
        if first_word in hero_list:
            return RawAbilityV2(class_name=class_name, **data)
        print(f"Unknown class name: {class_name}")
        return None

    try:
        raw_items = [
            parse(k, v)
            for k, v in raw_items.items()
            if "base" not in k
            and "dummy" not in k
            and ("generic" not in k or "citadel" in k)
            and isinstance(v, dict)
        ]
        raw_items = [item for item in raw_items if item is not None]
        abilities, weapons, upgrades = 0, 0, 0
        for item in raw_items:
            if isinstance(item, RawAbilityV2):
                abilities += 1
            elif isinstance(item, RawWeaponV2):
                weapons += 1
            elif isinstance(item, RawUpgradeV2):
                upgrades += 1
        print(f"Abilities: {abilities}, Weapons: {weapons}, Upgrades: {upgrades}")

        with open("test.json", "w") as f:
            json.dump(
                [item.model_dump(exclude_none=True) for item in raw_items], f, indent=4
            )
        print(raw_items[:2])
    except ValidationError as e:
        pprint(e.errors())
        raise e


if __name__ == "__main__":
    test_parse()
