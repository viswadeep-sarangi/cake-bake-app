from typing import Dict, List, Tuple, Union
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from cake_bake_app.config import config
import logging
from sqlalchemy import create_engine, event
from cake_bake_app.models import (
    Base,
    CakePreferencesModel,
    CakePreferences,
    CakeResponsibilities,
    Employees,
)
from sqlalchemy_utils import database_exists

from cake_bake_app.process import get_bakers_for_employees

_logger = logging.getLogger(__name__)


def _fk_pragma_on_connect(dbapi_con, _):
    dbapi_con.execute("pragma foreign_keys=ON")


engine = create_engine(
    f"sqlite:///{config.db_name}.db?check_same_thread={config.db_check_same_thread}",
    echo=True,
)
event.listen(engine, "connect", _fk_pragma_on_connect)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_db_schema(engine: Engine):
    _logger.info(f"Creating DB schema for engine {engine}")
    Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def add_employee_db(employee: Employees, session: Session) -> Employees:
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


def get_all_employees_db(session: Session) -> List[Employees]:
    return session.query(Employees).all()


def get_employee(name: str, session: Session) -> Employees:
    return session.query(Employees).filter(Employees.name == name).first()


def get_cake_preference_db(name: str, session: Session) -> CakePreferences:
    cake_pref = (
        session.query(CakePreferences).filter(CakePreferences.name == name).first()
    )
    return cake_pref


def add_cake_preference_db(
    cake_preference: CakePreferences, session: Session
) -> CakePreferences:
    session.add(cake_preference)
    session.commit()
    session.refresh(cake_preference)

    (all_done, names) = names_if_all_preferences_submitted(session)
    if all_done:
        baker_receivers = get_bakers_for_employees(names, session)
        add_cake_responsibilities_db(baker_receivers, session)

    return cake_preference


def add_cake_responsibilities_db(baker_receivers: Dict[str, str], session: Session):
    for baker, receiver in baker_receivers.items():
        orm = CakeResponsibilities(baker_name=baker, cake_receiver_name=receiver)
        session.add(orm)
    session.commit()


def all_cake_preferences_db(session: Session) -> List[CakePreferences]:
    all_cake_prefs = session.query(CakePreferences).all()
    return all_cake_prefs


def get_cake_preference_db(name: str, session: Session) -> CakePreferences:
    return session.query(CakePreferences).filter(CakePreferences.name == name).first()


def all_cake_responsibilities_db(
    session: Session,
) -> Union[List[CakeResponsibilities], Dict]:
    (all_done, names) = names_if_all_preferences_submitted(session)
    if not all_done:
        return {
            "message": "All employees have not yet submitted their preferences. Please check back later. "
            f"<br>Employees yet to submit:  {', '.join(names)}"
        }
    cake_resps = session.query(CakeResponsibilities).all()
    return cake_resps


def get_cake_responsibility_db(
    name: str, session: Session
) -> Union[CakeResponsibilities, Dict]:
    (all_done, names) = names_if_all_preferences_submitted(session)
    if not all_done:
        return {
            "message": "All employees have not yet submitted their preferences. Please check back later. "
            f"<br>Employees yet to submit:  {', '.join(names)}"
        }
    cake_resp = (
        session.query(CakeResponsibilities)
        .filter(CakeResponsibilities.baker_name == name)
        .first()
    )
    return cake_resp


def names_if_all_preferences_submitted(session: Session) -> Tuple[bool, List[str]]:
    employee_names = [r for (r,) in session.query(Employees.name).all()]
    submitter_names = [r for (r,) in session.query(CakePreferences.name).all()]
    if set(employee_names) == set(submitter_names):
        return (True, employee_names)
    return (False, list(set(employee_names) - set(submitter_names)))


def create_database_if_not_exists():
    if not database_exists(engine.url):
        create_db_schema(engine)
