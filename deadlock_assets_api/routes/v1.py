from fastapi import APIRouter, HTTPException

from deadlock_assets_api.models import colors
from deadlock_assets_api.models.colors import Color
from deadlock_assets_api.models.hero import Hero, load_heroes
from deadlock_assets_api.models.item import Item, ItemSlotType, ItemType, load_items
from deadlock_assets_api.models.languages import Language
from deadlock_assets_api.models.map import Map

router = APIRouter(prefix="/v1")


@router.get("/heroes", response_model_exclude_none=True)
def get_heroes(language: Language = Language.English) -> list[Hero]:
    heroes = load_heroes()
    for hero in heroes:
        hero.set_language(language)
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
        if hero.class_name.lower() == name.lower():
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@router.get("/items", response_model_exclude_none=True)
def get_items(language: Language = Language.English) -> list[Item]:
    items = load_items()
    for item in items:
        item.set_language(language)
        item.postfix(items)
    return items


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
    return [c for c in items if c.item_slot_type == slot_type]


@router.get("/map", response_model_exclude_none=True)
def get_map() -> Map:
    return Map.get_default()


@router.get("/colors", response_model_exclude_none=True)
def get_colors() -> dict[str, Color]:
    return colors.get_colors()
