import json
import os
from enum import Enum
from functools import lru_cache

from fastapi import APIRouter, HTTPException
from pydantic import TypeAdapter

from deadlock_assets_api import utils
from deadlock_assets_api.models.item import ItemSlotType, ItemType
from deadlock_assets_api.models.languages import Language
from deadlock_assets_api.models.v2.api_ability import Ability
from deadlock_assets_api.models.v2.api_hero import Hero
from deadlock_assets_api.models.v2.api_item import Item
from deadlock_assets_api.models.v2.api_upgrade import Upgrade
from deadlock_assets_api.models.v2.api_weapon import Weapon
from deadlock_assets_api.models.v2.raw_ability import RawAbility
from deadlock_assets_api.models.v2.raw_hero import RawHero
from deadlock_assets_api.models.v2.raw_upgrade import RawUpgrade
from deadlock_assets_api.models.v2.raw_weapon import RawWeapon

router = APIRouter(prefix="/v2", tags=["V2"])


@lru_cache
def load_localizations() -> dict[int, dict[Language, dict[str, str]]]:
    localizations = {}
    for client_version in ALL_CLIENT_VERSIONS:
        localizations[client_version] = {}
        for language in Language:
            localizations[client_version][language] = {}
            print(
                f"Loading localization for client version {client_version} and language {language}"
            )
            paths = [
                f"res/builds/{client_version}/v2/localization/citadel_gc_{language}.json",
                f"res/builds/{client_version}/v2/localization/citadel_heroes_{language}.json",
                f"res/builds/{client_version}/v2/localization/citadel_main_{language}.json",
            ]
            for path in paths:
                if not os.path.exists(path):
                    print(f"Path {path} does not exist")
                    continue
                with open(path) as f:
                    localizations[client_version][language].update(
                        json.load(f)["lang"]["Tokens"]
                    )
    return localizations


@lru_cache
def load_raw_heroes(client_version: int) -> list[RawHero] | None:
    path = f"res/builds/{client_version}/v2/raw_heroes.json"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        content = f.read()
    print(f"Loading raw heroes for client version {client_version}")
    return TypeAdapter(list[RawHero]).validate_json(content)


@lru_cache
def load_raw_items(
    client_version: int,
) -> list[RawAbility | RawWeapon | RawUpgrade] | None:
    path = f"res/builds/{client_version}/v2/raw_items.json"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        content = f.read()
    print(f"Loading raw items for client version {client_version}")
    return TypeAdapter(list[RawAbility | RawWeapon | RawUpgrade]).validate_json(content)


ALL_CLIENT_VERSIONS = [int(b) for b in os.listdir("res/builds")]
VALID_CLIENT_VERSIONS = Enum(
    "ValidClientVersions", {str(b): int(b) for b in ALL_CLIENT_VERSIONS}, type=int
)
LOCALIZATIONS: dict[int, dict[Language, dict[str, str]]] = load_localizations()
RAW_HEROES: dict[int, list[RawHero]] = {
    b: load_raw_heroes(b) for b in ALL_CLIENT_VERSIONS
}
RAW_ITEMS: dict[int, list[RawAbility | RawWeapon | RawUpgrade]] = {
    b: load_raw_items(b) for b in ALL_CLIENT_VERSIONS
}


@router.get("/heroes", response_model_exclude_none=True)
def get_heroes(
    language: Language = Language.English,
    client_version: VALID_CLIENT_VERSIONS = max(ALL_CLIENT_VERSIONS),
    only_active: bool = False,
) -> list[Hero]:
    if client_version not in ALL_CLIENT_VERSIONS:
        raise HTTPException(status_code=404, detail="Client Version not found")
    localization = {}
    if language != Language.English:
        localization.update(LOCALIZATIONS[client_version.value][Language.English])
    localization.update(LOCALIZATIONS[client_version.value][language])

    raw_heroes = RAW_HEROES[client_version.value]
    heroes = [
        Hero.from_raw_hero(r, localization)
        for r in raw_heroes
        if not only_active or not r.disabled
    ]
    return sorted(heroes, key=lambda x: x.id)


@router.get("/heroes/{id}", response_model_exclude_none=True)
def get_hero(
    id: int,
    language: Language = Language.English,
    client_version: VALID_CLIENT_VERSIONS = max(ALL_CLIENT_VERSIONS),
) -> Hero:
    heroes = get_heroes(language, client_version)
    for hero in heroes:
        if hero.id == id:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@router.get("/heroes/by-name/{name}", response_model_exclude_none=True)
def get_hero_by_name(
    name: str,
    language: Language = Language.English,
    client_version: VALID_CLIENT_VERSIONS = max(ALL_CLIENT_VERSIONS),
) -> Hero:
    heroes = get_heroes(language, client_version)
    for hero in heroes:
        if hero.class_name.lower() in [name.lower(), f"hero_{name.lower()}"]:
            return hero
        if hero.name.lower() in [name.lower(), f"hero_{name.lower()}"]:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@router.get("/items", response_model_exclude_none=True)
def get_items(
    language: Language = Language.English,
    client_version: VALID_CLIENT_VERSIONS = max(ALL_CLIENT_VERSIONS),
) -> list[Item]:
    if client_version not in ALL_CLIENT_VERSIONS:
        raise HTTPException(status_code=404, detail="Client Version not found")
    localization = {}
    if language != Language.English:
        localization.update(LOCALIZATIONS[client_version.value][Language.English])
    localization.update(LOCALIZATIONS[client_version.value][language])

    raw_items = RAW_ITEMS[client_version.value]
    raw_heroes = RAW_HEROES[client_version.value]

    def item_from_raw_item(raw_item: RawUpgrade | RawAbility | RawWeapon) -> Item:
        if raw_item.type == "ability":
            return Ability.from_raw_item(raw_item, raw_heroes, localization)
        elif raw_item.type == "upgrade":
            return Upgrade.from_raw_item(raw_item, raw_heroes, localization)
        elif raw_item.type == "weapon":
            return Weapon.from_raw_item(raw_item, raw_heroes, localization)
        else:
            raise ValueError(f"Unknown item type: {raw_item.type}")

    items = [item_from_raw_item(r) for r in raw_items]
    return sorted(items, key=lambda x: x.id)


@router.get("/items/{id_or_class_name}", response_model_exclude_none=True)
def get_item(
    id_or_class_name: int | str,
    language: Language = Language.English,
    client_version: VALID_CLIENT_VERSIONS = max(ALL_CLIENT_VERSIONS),
) -> Item:
    items = get_items(language, client_version=client_version)
    id = int(id_or_class_name) if utils.is_int(id_or_class_name) else id_or_class_name
    for item in items:
        if item.id == id or item.class_name == id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/items/by-hero-id/{id}", response_model_exclude_none=True)
def get_items_by_hero_id(
    id: int,
    language: Language = Language.English,
    client_version: VALID_CLIENT_VERSIONS = max(ALL_CLIENT_VERSIONS),
) -> list[Item]:
    items = get_items(language, client_version)
    return [i for i in items if i.hero == id]


@router.get("/items/by-type/{type}", response_model_exclude_none=True)
def get_items_by_type(
    type: ItemType,
    language: Language = Language.English,
    client_version: VALID_CLIENT_VERSIONS = max(ALL_CLIENT_VERSIONS),
) -> list[Item]:
    items = get_items(language, client_version)
    type = ItemType(type.capitalize())
    return [c for c in items if c.type == type]


@router.get("/items/by-slot-type/{slot_type}", response_model_exclude_none=True)
def get_items_by_slot_type(
    slot_type: ItemSlotType,
    language: Language = Language.English,
    client_version: VALID_CLIENT_VERSIONS = max(ALL_CLIENT_VERSIONS),
) -> list[Item]:
    items = get_items(language, client_version)
    slot_type = ItemSlotType(slot_type.capitalize())
    return [
        c for c in items if isinstance(c, Upgrade) and c.item_slot_type == slot_type
    ]


@router.get("/client-versions")
def get_client_versions() -> list[int]:
    return ALL_CLIENT_VERSIONS
