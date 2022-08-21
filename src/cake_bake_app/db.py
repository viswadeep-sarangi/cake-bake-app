
from sqlalchemy.engine import Engine
from config import config
import logging
from sqlalchemy import create_engine
from cake_bake_app.model import Base

_logger = logging.getLogger(__name__)

def create_db_engine()->Engine:
    engine = create_engine(f"sqlite:///{config.db_name}.db", echo=True)
    return engine

def create_db_schema(engine:Engine):
    _logger.info(f"Creating DB schema for engine {engine}")
    Base.metadata.create_all(engine)

# for debugging purposes only
if __name__=="__main__":
    engine = create_db_engine()
    create_db_schema(engine)