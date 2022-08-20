import logging
from fastapi import FastAPI
from . import ping
_logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    _logger.info("Initialising app...")
    app = FastAPI(title="Cake Bake App")

    _logger.info("Registering API routers...")
    app.include_router(ping.router, prefix="/ping", tags=["ping"])

    return app


app = create_app()

@app.on_event("startup")
async def startup_event() -> None:
    _logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    _logger.info("Shutting down...")
