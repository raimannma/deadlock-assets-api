import logging

from fastapi import FastAPI, HTTPException
from pydantic import TypeAdapter
from starlette.responses import RedirectResponse

from deadlock_assets_api.models.hero import Hero

logging.basicConfig(level=logging.INFO)
app = FastAPI()


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")


@app.get("/heroes", response_model_exclude_none=True)
def get_heroes() -> list[Hero]:
    with open("res/heroes.json") as f:
        content = f.read()
    ta = TypeAdapter(list[Hero])
    return ta.validate_json(content)


@app.get("/heroes/{id}", response_model_exclude_none=True)
def get_hero(id: int) -> Hero:
    heroes = get_heroes()
    for hero in heroes:
        if hero.id == id:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@app.get("/heroes/by-name/{name}", response_model_exclude_none=True)
def get_hero_by_name(name: str) -> Hero:
    heroes = get_heroes()
    for hero in heroes:
        if hero.name.lower() == name.lower():
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
