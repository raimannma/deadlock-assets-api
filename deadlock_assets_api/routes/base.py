from fastapi import APIRouter

from deadlock_assets_api.models.languages import Language
from deadlock_assets_api.models.v1.hero import HeroV1
from deadlock_assets_api.models.v1.item import ItemTypeV1, ItemV1
from deadlock_assets_api.routes import v1

router = APIRouter()


@router.get("/heroes", response_model_exclude_none=True)
def get_heroes(language: Language = Language.English) -> list[HeroV1]:
    return v1.get_heroes(language)


@router.get("/heroes/{id}", response_model_exclude_none=True)
def get_hero(id: int, language: Language = Language.English) -> HeroV1:
    return v1.get_hero(id, language)


@router.get("/heroes/by-name/{name}", response_model_exclude_none=True)
def get_hero_by_name(name: str, language: Language = Language.English) -> HeroV1:
    return v1.get_hero_by_name(name, language)


@router.get("/items", response_model_exclude_none=True)
def get_items(language: Language = Language.English) -> list[ItemV1]:
    return v1.get_items(language)


@router.get("/items/{id}", response_model_exclude_none=True)
def get_item(id: int, language: Language = Language.English) -> ItemV1:
    return v1.get_item(id, language)


@router.get("/items/by-name/{name}", response_model_exclude_none=True)
def get_item_by_name(name: str, language: Language = Language.English) -> ItemV1:
    return v1.get_item_by_name(name, language)


@router.get("/items/by-type/{type}", response_model_exclude_none=True)
def get_items_by_type(type: ItemTypeV1, language: Language = Language.English) -> list[ItemV1]:
    return v1.get_items_by_type(type, language)
