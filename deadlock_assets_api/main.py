import logging
import os

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from deadlock_assets_api.models.hero import Hero, load_heroes
from deadlock_assets_api.models.item import Item, ItemType, load_items
from deadlock_assets_api.models.languages import Language

logging.basicConfig(level=logging.INFO)
IMAGE_BASE_URL = os.environ.get("IMAGE_BASE_URL")

app = FastAPI(
    title="Deadlock Assets API",
    description="API for Deadlock assets, including hero stats and images, and item stats and images.",
)

Instrumentator().instrument(app).expose(app, include_in_schema=False)


@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    is_success = 200 <= response.status_code < 300
    is_docs = request.url.path.replace("/", "").startswith("docs")
    if is_success and not is_docs:
        response.headers["Cache-Control"] = "public, max-age=3600"
    return response


if IMAGE_BASE_URL is None:
    app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")


@app.get("/heroes", response_model_exclude_none=True)
def get_heroes(request: Request, language: Language = Language.English) -> list[Hero]:
    heroes = load_heroes()
    for hero in heroes:
        hero.set_base_url(
            IMAGE_BASE_URL or str(request.base_url).replace("http://", "https://")
        )
        hero.set_language(language)
    heroes = [h for h in heroes if not h.disabled]
    heroes = sorted(heroes, key=lambda x: x.id)
    return heroes


@app.get("/heroes/{id}", response_model_exclude_none=True)
def get_hero(request: Request, id: int, language: Language = Language.English) -> Hero:
    heroes = get_heroes(request, language)
    for hero in heroes:
        if hero.id == id:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@app.get("/heroes/by-name/{name}", response_model_exclude_none=True)
def get_hero_by_name(
    request: Request, name: str, language: Language = Language.English
) -> Hero:
    heroes = get_heroes(request, language)
    for hero in heroes:
        if hero.class_name.lower() == name.lower():
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@app.get("/items", response_model_exclude_none=True)
def get_items(request: Request, language: Language = Language.English) -> list[Item]:
    items = load_items()
    for item in items:
        item.set_base_url(
            IMAGE_BASE_URL or str(request.base_url).replace("http://", "https://")
        )
        item.set_language(language)
        item.postfix(items)
    return items


@app.get("/items/{id}", response_model_exclude_none=True)
def get_item(request: Request, id: int, language: Language = Language.English) -> Item:
    items = get_items(request, language)
    for item in items:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/by-name/{name}", response_model_exclude_none=True)
def get_item_by_name(
    request: Request, name: str, language: Language = Language.English
) -> Item:
    items = get_items(request, language)
    for item in items:
        if name.lower() in [item.name.lower(), item.class_name.lower()]:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/by-type/{type}", response_model_exclude_none=True)
def get_items_by_type(
    request: Request, type: ItemType, language: Language = Language.English
) -> list[Item]:
    items = get_items(request, language)
    type = ItemType(type.capitalize())
    return [c for c in items if c.type == type]


@app.get("/health", include_in_schema=False)
def get_health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
