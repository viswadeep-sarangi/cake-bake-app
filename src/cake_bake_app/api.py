
from typing import Dict, List
from fastapi import APIRouter, Depends, Request

from cake_bake_app.models import CakePreferencesModel, EmployeeRequestModel, Employees, EmployeesModel
from cake_bake_app.models import CakePreferences
from cake_bake_app.db import add_cake_preference_db, add_employee_db, all_cake_preferences_db, all_cake_responsibilities_db, get_all_employees_db, get_cake_preference_db, get_cake_responsibility_db, get_session

router = APIRouter()

@router.post("/add_employee", summary="Add an employee with date of birth")
async def add_employee(request_body:EmployeesModel, session=Depends(get_session)):
    """Add an employee with date of birth"""
    employee_orm = Employees(**dict(request_body))
    employee_orm = add_employee_db(employee=employee_orm, session=session)
    return {"message":f"{request_body.name} added to database   {employee_orm.as_dict()}"}

@router.get("/employees", summary="Get all employees")
def all_employees(session=Depends(get_session)):
    return get_all_employees_db(session)

@router.post("/submit_preferences", summary="Submit cake preferences")
async def submit_preferences(request_body:CakePreferencesModel, session=Depends(get_session)):
    """Submit cake preferences"""
    cake_pref_orm = CakePreferences(**dict(request_body))
    print(request_body)
    print(cake_pref_orm)
    cake_pref_orm = add_cake_preference_db(cake_preference=cake_pref_orm, session=session)
    return {"message": f"Cake preferences for {request_body.name} added to database     {cake_pref_orm.as_dict()}"}

@router.post("/employee_preferences", summary="Get cake preference for an employee")
async def get_employee_cake_preference(request_body:EmployeeRequestModel, session=Depends(get_session)):    
    return get_cake_preference_db(request_body.name, session)

@router.get("/preferences", summary="Get all cake preferences")
async def get_all_cake_preferences(session=Depends(get_session))->List[CakePreferences]:
    """Get all cake preferences"""
    all_cake_prefs = all_cake_preferences_db(session=session)
    return all_cake_prefs

@router.get("/baking_responsibilities", summary="Get all cake baking responbilities")
async def get_all_baking_responsibilities(session=Depends(get_session)):
    """Get all cake baking responbilities"""
    cake_resps = all_cake_responsibilities_db(session)
    return cake_resps

@router.post("/employee_baking_responsibillity", summary="Get cake baking responbilities")
async def get_cake_responsibility(request_body:EmployeeRequestModel, session=Depends(get_session)):
    """Get cake baking responbilities"""
    return get_cake_responsibility_db(request_body.name, session)