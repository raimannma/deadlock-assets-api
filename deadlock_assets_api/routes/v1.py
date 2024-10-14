import os
from functools import lru_cache

from fastapi import APIRouter, HTTPException

from deadlock_assets_api.glob import SVGS_BASE_URL
from deadlock_assets_api.models import colors
from deadlock_assets_api.models.colors import Color
from deadlock_assets_api.models.hero import Hero, load_heroes
from deadlock_assets_api.models.item import Item, ItemSlotType, ItemType, load_items
from deadlock_assets_api.models.languages import Language
from deadlock_assets_api.models.map import Map
from deadlock_assets_api.models.steam_info import SteamInfo

router = APIRouter(prefix="/v1", tags=["V1"])


@router.get(
    "/heroes",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/heroes` instead.",
)
def get_heroes(language: Language = Language.English) -> list[Hero]:
    heroes = load_heroes()
    for hero in heroes:
        hero.set_language(language)
    return sorted(heroes, key=lambda x: x.id)


@router.get(
    "/heroes/{id}",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/heroes/{id}` instead.",
)
def get_hero(id: int, language: Language = Language.English) -> Hero:
    heroes = get_heroes(language)
    for hero in heroes:
        if hero.id == id:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@router.get(
    "/heroes/by-name/{name}",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/heroes/by-name/{name}` instead.",
)
def get_hero_by_name(name: str, language: Language = Language.English) -> Hero:
    heroes = get_heroes(language)
    for hero in heroes:
        if hero.class_name.lower() == name.lower():
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@router.get(
    "/items",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/items` instead.",
)
def get_items(language: Language = Language.English) -> list[Item]:
    items = load_items()
    heroes = load_heroes()
    hero_weapons = {i for h in heroes for i in h.items.values()}
    for item in items:
        item.set_language(language)
        item.set_shopable()
        if item.shopable and (
            item.id in hero_weapons or item.class_name in hero_weapons
        ):
            item.shopable = False
        item.postfix(items)
    return items


@router.get(
    "/items/{id}",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/items/{id}` instead.",
)
def get_item(id: int, language: Language = Language.English) -> Item:
    items = get_items(language)
    for item in items:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.get(
    "/items/by-name/{name}",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/items/{name}` instead.",
)
def get_item_by_name(name: str, language: Language = Language.English) -> Item:
    items = get_items(language)
    for item in items:
        if name.lower() in [item.name.lower(), item.class_name.lower()]:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.get(
    "/items/by-hero-id/{id}",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/items/by-hero-id/{id}` instead.",
)
def get_items_by_hero_id(
    id: int, language: Language = Language.English
) -> dict[str, Item]:
    hero = get_hero(id, language)
    hero_item_ids = set(hero.items.values())
    hero_items = (i for i in get_items(language) if i.id in hero_item_ids)
    return dict(zip(hero.items.keys(), hero_items))


@router.get(
    "/items/by-hero-name/{name}",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/items/by-hero-id/{id}` instead.",
)
def get_items_by_hero_name(
    name: str, language: Language = Language.English
) -> dict[str, Item]:
    hero = get_hero_by_name(name, language)
    hero_item_ids = set(hero.items.values())
    hero_items = (i for i in get_items(language) if i.id in hero_item_ids)
    return dict(zip(hero.items.keys(), hero_items))


@router.get(
    "/items/by-type/{type}",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/items/by-type/{type}` instead.",
)
def get_items_by_type(
    type: ItemType, language: Language = Language.English
) -> list[Item]:
    items = get_items(language)
    type = ItemType(type.capitalize())
    return [c for c in items if c.type == type]


@router.get(
    "/items/by-slot-type/{slot_type}",
    response_model_exclude_none=True,
    deprecated=True,
    description="This endpoint is deprecated. Use `/v2/items/by-slot-type/{slot_type}` instead.",
)
def get_items_by_slot_type(
    slot_type: ItemSlotType, language: Language = Language.English
) -> list[Item]:
    items = get_items(language)
    slot_type = ItemSlotType(slot_type.capitalize())
    return [c for c in items if c.item_slot_type == slot_type]


@router.get("/map", response_model_exclude_none=True)
def get_map() -> Map:
    return Map.get_default()


@router.get("/colors", response_model_exclude_none=True)
def get_colors() -> dict[str, Color]:
    return colors.get_colors()


@router.get("/steam-info")
def get_steam_info() -> SteamInfo:
    return SteamInfo.load()


@router.get("/icons", response_model_exclude_none=True)
def get_icons() -> dict[str, str]:
    return {i.rstrip(".svg"): f"{SVGS_BASE_URL}/{i}" for i in get_all_icons()}


@lru_cache
def get_all_icons() -> list[str]:
    return [i for i in os.listdir("svgs") if i.endswith(".svg")]
