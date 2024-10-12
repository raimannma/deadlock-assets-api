import json
import os
from functools import lru_cache

from fastapi import APIRouter, HTTPException
from pydantic import TypeAdapter

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

router = APIRouter(prefix="/v2", tags=["V2 - Preview (Please report all bugs)"])


@lru_cache
def load_localizations() -> dict[int, dict[Language, dict[str, str]]]:
    localizations = {}
    for build in ALL_BUILDS:
        localizations[build] = {}
        for language in Language:
            localizations[build][language] = {}
            print(f"Loading localization for build {build} and language {language}")
            paths = [
                f"res/builds/{build}/v2/localization/citadel_gc_{language}.json",
                f"res/builds/{build}/v2/localization/citadel_heroes_{language}.json",
                f"res/builds/{build}/v2/localization/citadel_main_{language}.json",
            ]
            for path in paths:
                if not os.path.exists(path):
                    print(f"Path {path} does not exist")
                    continue
                with open(path) as f:
                    localizations[build][language].update(
                        json.load(f)["lang"]["Tokens"]
                    )
    return localizations


@lru_cache
def load_raw_heroes(build_id: int) -> list[RawHero] | None:
    path = f"res/builds/{build_id}/v2/raw_heroes.json"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        content = f.read()
    print(f"Loading raw heroes for build {build_id}")
    return TypeAdapter(list[RawHero]).validate_json(content)


@lru_cache
def load_raw_items(build_id: int) -> list[RawAbility | RawWeapon | RawUpgrade] | None:
    path = f"res/builds/{build_id}/v2/raw_items.json"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        content = f.read()
    print(f"Loading raw items for build {build_id}")
    return TypeAdapter(list[RawAbility | RawWeapon | RawUpgrade]).validate_json(content)


ALL_BUILDS = [int(b) for b in os.listdir("res/builds")]
LOCALIZATIONS: dict[int, dict[Language, dict[str, str]]] = load_localizations()
RAW_HEROES: dict[int, list[RawHero]] = {b: load_raw_heroes(b) for b in ALL_BUILDS}
RAW_ITEMS: dict[int, list[RawAbility | RawWeapon | RawUpgrade]] = {
    b: load_raw_items(b) for b in ALL_BUILDS
}


@router.get("/heroes", response_model_exclude_none=True)
def get_heroes(
    language: Language = Language.English, build_id: int = max(ALL_BUILDS)
) -> list[Hero]:
    localization = {}
    if language != Language.English:
        localization.update(LOCALIZATIONS[build_id][Language.English])
    localization.update(LOCALIZATIONS[build_id][language])

    raw_heroes = RAW_HEROES[build_id]
    heroes = [Hero.from_raw_hero(r, localization) for r in raw_heroes]
    return sorted(heroes, key=lambda x: x.id)


@router.get("/heroes/{id}", response_model_exclude_none=True)
def get_hero(id: int, language: Language = Language.English) -> Hero:
    heroes = get_heroes(language)
    for hero in heroes:
        if hero.id == id:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@router.get("/heroes/by-name/{name}", response_model_exclude_none=True)
def get_hero_by_name(name: str, language: Language = Language.English) -> Hero:
    heroes = get_heroes(language)
    for hero in heroes:
        if hero.class_name.lower() in [name.lower(), f"hero_{name.lower()}"]:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@router.get("/items", response_model_exclude_none=True)
def get_items(
    language: Language = Language.English, build_id: int = max(ALL_BUILDS)
) -> list[Item]:
    localization = {}
    if language != Language.English:
        localization.update(LOCALIZATIONS[build_id][Language.English])
    localization.update(LOCALIZATIONS[build_id][language])

    raw_items = RAW_ITEMS[build_id]
    raw_heroes = RAW_HEROES[build_id]

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


@router.get("/items/{id}", response_model_exclude_none=True)
def get_item(id: int, language: Language = Language.English) -> Item:
    items = get_items(language)
    for item in items:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/items/by-name/{name}", response_model_exclude_none=True)
def get_item_by_name(name: str, language: Language = Language.English) -> Item:
    items = get_items(language)
    for item in items:
        if name.lower() in [item.name.lower(), item.class_name.lower()]:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/items/by-hero-id/{id}", response_model_exclude_none=True)
def get_items_by_hero_id(id: int, language: Language = Language.English) -> list[Item]:
    items = get_items(language)
    return [i for i in items if i.hero == id]


@router.get("/items/by-type/{type}", response_model_exclude_none=True)
def get_items_by_type(
    type: ItemType, language: Language = Language.English
) -> list[Item]:
    items = get_items(language)
    type = ItemType(type.capitalize())
    return [c for c in items if c.type == type]


@router.get("/items/by-slot-type/{slot_type}", response_model_exclude_none=True)
def get_items_by_slot_type(
    slot_type: ItemSlotType, language: Language = Language.English
) -> list[Item]:
    items = get_items(language)
    slot_type = ItemSlotType(slot_type.capitalize())
    return [
        c for c in items if isinstance(c, Upgrade) and c.item_slot_type == slot_type
    ]
