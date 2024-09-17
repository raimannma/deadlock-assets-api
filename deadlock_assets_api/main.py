import logging
import os

from fastapi import FastAPI, HTTPException
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from deadlock_assets_api.models.hero import Hero
from deadlock_assets_api.models.item import Item, ItemType

logging.basicConfig(level=logging.INFO)
IMAGE_BASE_URL = os.environ.get("IMAGE_BASE_URL")

app = FastAPI()


@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    if not request.url.path.replace("/", "").startswith("docs"):
        response.headers["Cache-Control"] = "public, max-age=3600"
    return response


if IMAGE_BASE_URL is None:
    app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")


@app.get("/heroes", response_model_exclude_none=True)
def get_heroes(request: Request) -> list[Hero]:
    with open("res/heroes.json") as f:
        content = f.read()
    ta = TypeAdapter(list[Hero])
    heroes = ta.validate_json(content)
    for hero in heroes:
        hero.set_base_url(
            IMAGE_BASE_URL or str(request.base_url).replace("http://", "https://")
        )
    return heroes


@app.get("/heroes/{id}", response_model_exclude_none=True)
def get_hero(request: Request, id: int) -> Hero:
    heroes = get_heroes(request)
    for hero in heroes:
        if hero.id == id:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@app.get("/heroes/by-name/{name}", response_model_exclude_none=True)
def get_hero_by_name(request: Request, name: str) -> Hero:
    heroes = get_heroes(request)
    for hero in heroes:
        if hero.name.lower() == name.lower():
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@app.get("/items", response_model_exclude_none=True)
def get_items(request: Request) -> list[Item]:
    with open("res/items.json") as f:
        content = f.read()
    ta = TypeAdapter(list[Item])
    items = ta.validate_json(content)
    for c in items:
        c.set_base_url(
            IMAGE_BASE_URL or str(request.base_url).replace("http://", "https://")
        )
    return items


@app.get("/items/{id}", response_model_exclude_none=True)
def get_item(request: Request, id: int) -> Item:
    items = get_items(request)
    for item in items:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/by-name/{name}", response_model_exclude_none=True)
def get_items_by_name(request: Request, name: str) -> Item:
    items = get_items(request)
    for item in items:
        if item.name.lower() == name.lower():
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/by-type/{type}", response_model_exclude_none=True)
def get_items_by_type(request: Request, type: ItemType) -> list[Item]:
    items = get_items(request)
    type = ItemType(type.capitalize())
    return [c for c in items if c.type == type]


@app.get("/health", include_in_schema=False)
def get_health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
