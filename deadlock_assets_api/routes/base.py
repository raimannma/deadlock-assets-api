from fastapi import APIRouter
from starlette.requests import Request

from deadlock_assets_api.models.hero import Hero
from deadlock_assets_api.models.item import Item, ItemType
from deadlock_assets_api.models.languages import Language
from deadlock_assets_api.routes import v1

router = APIRouter()


@router.get("/heroes", response_model_exclude_none=True)
def get_heroes(request: Request, language: Language = Language.English) -> list[Hero]:
    return v1.get_heroes(request, language)


@router.get("/heroes/{id}", response_model_exclude_none=True)
def get_hero(request: Request, id: int, language: Language = Language.English) -> Hero:
    return v1.get_hero(request, id, language)


@router.get("/heroes/by-name/{name}", response_model_exclude_none=True)
def get_hero_by_name(
    request: Request, name: str, language: Language = Language.English
) -> Hero:
    return v1.get_hero_by_name(request, name, language)


@router.get("/items", response_model_exclude_none=True)
def get_items(request: Request, language: Language = Language.English) -> list[Item]:
    return v1.get_items(request, language)


@router.get("/items/{id}", response_model_exclude_none=True)
def get_item(request: Request, id: int, language: Language = Language.English) -> Item:
    return v1.get_item(request, id, language)


@router.get("/items/by-name/{name}", response_model_exclude_none=True)
def get_item_by_name(
    request: Request, name: str, language: Language = Language.English
) -> Item:
    return v1.get_item_by_name(request, name, language)


@router.get("/items/by-type/{type}", response_model_exclude_none=True)
def get_items_by_type(
    request: Request, type: ItemType, language: Language = Language.English
) -> list[Item]:
    return v1.get_items_by_type(request, type, language)
