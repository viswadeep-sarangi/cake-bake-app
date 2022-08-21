
from http.client import HTTPException
from typing import Dict, List, Union
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from cake_bake_app.config import config
import logging
from sqlalchemy import create_engine, event
from cake_bake_app.models import Base, CakePreferencesModel, CakePreferences, CakeResponsibilities, Employees
from sqlalchemy_utils import database_exists

from cake_bake_app.process import get_bakers_for_employees

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

    names = names_if_all_preferences_submitted(session)
    if names is not None:
        baker_receivers = get_bakers_for_employees(names)
        add_cake_responsibilities_db(baker_receivers, session)

    return cake_preference

def add_cake_responsibilities_db(baker_receivers:Dict[str,str],session:Session):
    for baker, receiver in baker_receivers.items():
        orm = CakeResponsibilities(
            baker_name=baker,
            cake_receiver_name=receiver
        )
        session.add(orm)
    session.commit()


# def update_cake_preference(new_cake_preference:CakePreferencesOrm, session:Session = get_session())->CakePreferencesOrm:
#     cake_pref = get_cake_preference(name=new_cake_preference.name, session=session)
#     if not cake_pref:
#             raise HTTPException(status_code=404, detail=f"Existing preferences not found for {new_cake_preference.name}")
#     cake_pref.

def all_cake_preferences_db(session:Session)->List[CakePreferences]:
    all_cake_prefs = session.query(CakePreferences).all()
    return all_cake_prefs

def get_cake_preference_db(name:str, session:Session)->CakePreferences:
    return session.query(CakePreferences).filter(CakePreferences.name==name).first()

def all_cake_responsibilities_db(session:Session)->Union[List[CakeResponsibilities],Dict]:
    names = names_if_all_preferences_submitted(session)
    if names is None:
        return {"message":"All employees have not yet submitted their preferences. Please check back later"}
    cake_resps = session.query(CakeResponsibilities).all()
    return cake_resps


def get_cake_responsibility_db(name:str, session:Session) ->CakeResponsibilities:
    if names_if_all_preferences_submitted(session) is None:
        return {"message":"All employees have not yet submitted their preferences. Please check back later"}
    cake_resp = session.query(CakeResponsibilities).filter(CakeResponsibilities.baker_name==name).first()
    return cake_resp

def names_if_all_preferences_submitted(session:Session)->bool:
    employee_names = [r for (r,) in session.query(Employees.name).all()]
    submitter_names = [r for (r,) in session.query(CakePreferences.name).all()]
    if set(employee_names)==set(submitter_names):
        return employee_names
    return None


def create_database_if_not_exists():
    if not database_exists(engine.url):
        create_db_schema(engine)

# # for debugging purposes only
# if __name__=="__main__":
#     create_db_schema(engine)