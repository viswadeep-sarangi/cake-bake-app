
from datetime import datetime
from sqlalchemy import Column, String, Table, DateTime, ForeignKey, Boolean
from typing import Dict
from pydantic import BaseModel
import re
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

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

    # @declared_attr
    # def as_dict(cls:Any) -> Dict[str,str]:
    #    return {c.name: getattr(cls, c.name) for c in cls.__table__.columns}

class Employees(Base):
    name = Column(String, primary_key=True)
    date_of_birth = Column(DateTime)

class CakePreferences(Base):
    name = Column(String, ForeignKey(f"employees.name"), primary_key=True)
    food_intolerence = Column(String)
    cake_preference = Column(String)
    can_bake = Column(Boolean)
    can_provide_ingredients = Column(Boolean)
        
class EmployeesModel(BaseModel):
    name:str
    date_of_birth:datetime

class CakePreferencesModel(BaseModel):
    name:str
    food_intolerence:str
    cake_preference:str
    can_bake:bool
    can_provide_ingredients:bool