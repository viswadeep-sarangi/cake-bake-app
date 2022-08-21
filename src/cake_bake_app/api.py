
from typing import Dict, List
from fastapi import APIRouter, Depends

from cake_bake_app.models import CakePreferencesModel, Employees, EmployeesModel
from cake_bake_app.models import CakePreferences
from cake_bake_app.db import add_cake_preference_db, add_employee_db, all_cake_preferences_db, get_session

router = APIRouter()

@router.post("/add_employee", summary="Add an employee with date of birth")
async def add_employee(request_body:EmployeesModel, session=Depends(get_session)):
    """Add an employee with date of birth"""
    employee_orm = Employees(**dict(request_body))
    employee_orm = add_employee_db(employee=employee_orm, session=session)

@router.post("/submit_preferences", summary="Submit cake preferences")
async def submit_preferences(request_body:CakePreferencesModel, session=Depends(get_session)):
    """Submit cake preferences"""
    cake_pref_orm = CakePreferences(**dict(request_body))
    print(request_body)
    print(cake_pref_orm)
    cake_pref_orm = add_cake_preference_db(cake_preference=cake_pref_orm, session=session)
    return {"message": "test"}


@router.get("/preferences", summary="Get all cake baking responbilities")
async def get_all_cake_preferences(session=Depends(get_session))->List[Dict[str,str]]:
    """Get all cake baking responbilities"""
    all_cake_prefs = all_cake_preferences_db(session=session)
    return all_cake_prefs


@router.post("/baking_responsibillity", summary="Get cake baking responbilities")
async def get_cake_responsibility(name:str):
    """Get cake baking responbilities"""
    return {"message":"test"}