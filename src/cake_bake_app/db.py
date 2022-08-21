
from http.client import HTTPException
from typing import List
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from config import config
import logging
from sqlalchemy import create_engine, event
from cake_bake_app.model import Base, CakePreferencesModel, CakePreferences, Employees

_logger = logging.getLogger(__name__)


def _fk_pragma_on_connect(dbapi_con, _):
    dbapi_con.execute('pragma foreign_keys=ON')

engine = create_engine(f"sqlite:///{config.db_name}.db?check_same_thread={config.db_check_same_thread}", echo=True)
event.listen(engine, 'connect', _fk_pragma_on_connect)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def create_db_schema(engine:Engine):
    _logger.info(f"Creating DB schema for engine {engine}")
    Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def add_employee_db(employee:Employees, session:Session)->Employees:
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def get_cake_preference_db(name:str, session:Session)->CakePreferences:
    cake_pref = session.query(CakePreferences).filter(CakePreferences.name==name).first()
    return cake_pref

def add_cake_preference_db(cake_preference:CakePreferences, session:Session)->CakePreferences:
    session.add(cake_preference)
    session.commit()
    session.refresh(cake_preference)
    return cake_preference

# def update_cake_preference(new_cake_preference:CakePreferencesOrm, session:Session = get_session())->CakePreferencesOrm:
#     cake_pref = get_cake_preference(name=new_cake_preference.name, session=session)
#     if not cake_pref:
#             raise HTTPException(status_code=404, detail=f"Existing preferences not found for {new_cake_preference.name}")
#     cake_pref.

def all_cake_preferences_db(session:Session)->List[CakePreferences]:
    all_cake_prefs = session.query(CakePreferences).all()
    return all_cake_prefs

# for debugging purposes only
if __name__=="__main__":
    create_db_schema(engine)