import uvicorn
from cake_bake_app.config import config
import logging
from cake_bake_app.db import create_database_if_not_exists

_logger = logging.getLogger(__name__)


def main() -> None:
    create_database_if_not_exists()
    uvicorn.run(
        "cake_bake_app.app:app",
        port=config.api_port,
        host=config.api_host,
        workers=config.api_worker_count,
    )
    _logger.info(f"Serving on port {config.api_port}")


if __name__ == "__main__":
    main()
