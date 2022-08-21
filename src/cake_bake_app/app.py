import logging
from fastapi import FastAPI
from cake_bake_app import ping
from cake_bake_app import api
from cake_bake_app import html
from fastapi.responses import RedirectResponse

_logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    _logger.info("Initialising app...")
    app = FastAPI(title="Cake Bake App")

    _logger.info("Registering API routers...")
    app.include_router(ping.router, prefix="/ping", tags=["ping"])
    app.include_router(api.router, prefix="/cake", tags=["cake"])
    app.include_router(html.router, prefix="/html", tags=["html"])

    return app

app = create_app()

@app.get("/")
async def redirect_html():
    return RedirectResponse(url="/html/add_employee")

@app.on_event("startup")
async def startup_event() -> None:
    _logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    _logger.info("Shutting down...")
