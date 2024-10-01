import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.staticfiles import StaticFiles

from deadlock_assets_api.routes import base, raw, v1

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Deadlock Assets API",
    description="API for Deadlock assets, including hero stats and images, and item stats and images.",
)

Instrumentator().instrument(app).expose(app, include_in_schema=False)

app.include_router(base.router, include_in_schema=False)
app.include_router(v1.router)
app.include_router(raw.router)


@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    if "Cache-Control" in response.headers:
        return response

    is_success = 200 <= response.status_code < 300
    is_docs = request.url.path.replace("/", "").startswith("docs")
    is_health = request.url.path.replace("/", "").startswith("health")
    if is_success and not is_docs and not is_health:
        response.headers["Cache-Control"] = "public, max-age=86400"
    return response


class StaticFilesCache(StaticFiles):
    def file_response(self, *args, **kwargs) -> Response:
        resp: Response = super().file_response(*args, **kwargs)
        resp.headers.setdefault(
            "Cache-Control", "public, max-age=604800, s-maxage=604800, immutable"
        )
        return resp


app.mount("/images", StaticFilesCache(directory="images"), name="images")
app.mount("/videos", StaticFilesCache(directory="videos"), name="videos")


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")


@app.get("/health", include_in_schema=False)
def get_health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
