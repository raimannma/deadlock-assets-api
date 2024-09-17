import logging
import os

from fastapi import FastAPI, HTTPException
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from deadlock_assets_api.models.ability import Ability
from deadlock_assets_api.models.hero import Hero

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

IMAGE_BASE_URL = os.environ.get("IMAGE_BASE_URL")


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


@app.get("/abilities", response_model_exclude_none=True)
def get_abilities(request: Request) -> list[Ability]:
    with open("res/abilities.json") as f:
        content = f.read()
    ta = TypeAdapter(list[Ability])
    abilities = ta.validate_json(content)
    for ability in abilities:
        ability.set_base_url(
            IMAGE_BASE_URL or str(request.base_url).replace("http://", "https://")
        )
    return abilities


@app.get("/abilities/{name}", response_model_exclude_none=True)
def get_ability(request: Request, name: str) -> Ability:
    abilities = get_abilities(request)
    for ability in abilities:
        if ability.name.lower() == name.lower():
            return ability
    raise HTTPException(status_code=404, detail="Ability not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
