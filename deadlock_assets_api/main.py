import logging
import os

from fastapi import FastAPI, HTTPException
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from deadlock_assets_api.models.component import Component, ComponentType
from deadlock_assets_api.models.hero import Hero

logging.basicConfig(level=logging.INFO)
IMAGE_BASE_URL = os.environ.get("IMAGE_BASE_URL")

app = FastAPI()


@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
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


@app.get("/components", response_model_exclude_none=True)
def get_components(request: Request) -> list[Component]:
    with open("res/components.json") as f:
        content = f.read()
    ta = TypeAdapter(list[Component])
    components = ta.validate_json(content)
    for c in components:
        c.set_base_url(
            IMAGE_BASE_URL or str(request.base_url).replace("http://", "https://")
        )
    return components


@app.get("/components/{id}", response_model_exclude_none=True)
def get_component(request: Request, id: int) -> Component:
    components = get_components(request)
    for component in components:
        if component.id == id:
            return component
    raise HTTPException(status_code=404, detail="Component not found")


@app.get("/components/by-name/{name}", response_model_exclude_none=True)
def get_components_by_name(request: Request, name: str) -> Component:
    components = get_components(request)
    for component in components:
        if component.name.lower() == name.lower():
            return component
    raise HTTPException(status_code=404, detail="Component not found")


@app.get("/components/by-type/{type}", response_model_exclude_none=True)
def get_components_by_type(request: Request, type: ComponentType) -> list[Component]:
    components = get_components(request)
    type = ComponentType(type.capitalize())
    return [c for c in components if c.type == type]


@app.get("/health", include_in_schema=False)
def get_health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
