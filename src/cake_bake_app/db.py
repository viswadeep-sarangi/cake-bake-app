import re
from typing import Any
from venv import create
from sqlalchemy import create_engine, MetaData, Column, String, Table, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.engine import Engine
from config import config
import logging

_logger = logging.getLogger(__name__)

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls: Any) -> str:
        """Takes the name of the Class with CamelCase and converts it into snake_case. This means we
        can use the class name.

        Returns:
            [type]: [description]

        """
        return re.sub("(?!^)([A-Z]+)", r"_\1", cls.__name__).lower()

class Employees(Base):
    name = Column(String, primary_key=True)
    date_of_birth = Column(DateTime)

class CakePreferences(Base):
    name = Column(String, ForeignKey(f"employees.name"), primary_key=True)
    food_intolerence = Column(String)
    cake_preference = Column(String)
    can_bake = Column(Boolean)
    can_provide_ingredients = Column(String)
    
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