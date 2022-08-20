import uvicorn
from config import config
import logging

_logger = logging.getLogger(__name__)

def main() -> None:
    uvicorn.run(
        "cake_bake_app.app:app",
        port=config.api_port,
        host=config.api_host,
        workers=config.api_worker_count,
    )
    _logger.info(f"Serving on port {config.api_port}")


if __name__ == "__main__":
    main()
