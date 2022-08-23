from asyncio import FastChildWatcher
from typing import Dict
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from cake_bake_app.template import (
    generate_add_employee_template,
    generate_show_cake_responsibility_template,
    generate_test_html_response,
    generate_submit_preference_template,
)
from cake_bake_app.template import generate_cake_responsibility_template
from cake_bake_app.models import (
    CakePreferences,
    EmployeeRequestModel,
    CakeResponsibilities,
    Employees,
)
from cake_bake_app.db import (
    get_cake_preference_db,
    get_employee,
    get_session,
    get_cake_responsibility_db,
)
from fastapi import Depends
from fastapi.exceptions import HTTPException

router = APIRouter()


@router.get("/test", summary="HTML test endpoint", response_class=HTMLResponse)
async def test() -> HTMLResponse:
    return generate_test_html_response()


@router.get(
    "/add_employee", summary="Add employee HTML endpoint", response_class=HTMLResponse
)
async def add_employee() -> HTMLResponse:
    return generate_add_employee_template()


@router.get(
    "/submit_preference", summary="Add cake preference", response_class=HTMLResponse
)
async def submit_preference() -> HTMLResponse:
    return generate_submit_preference_template()


@router.get(
    "/cake_responsibility", summary="Get cake pref", response_class=HTMLResponse
)
async def get_cake_resp() -> HTMLResponse:
    return generate_cake_responsibility_template()


@router.post(
    "/show_cake_responsibility",
    summary="Show cake responsibility",
    response_class=HTMLResponse,
)
async def show_cake_responsibility(
    request: EmployeeRequestModel, session=Depends(get_session)
) -> HTMLResponse:
    resp = get_cake_responsibility_db(request.name, session)
    if type(resp) == CakeResponsibilities:
        cake_pref: CakePreferences = get_cake_preference_db(
            name=resp.cake_receiver_name, session=session
        )
        emp: Employees = get_employee(name=resp.cake_receiver_name, session=session)
        cake_resp = {
            "baker_name": request.name,
            "cake_receiver": f"Name: {cake_pref.name}"
            f"<br>Food intolerences: {cake_pref.food_intolerence}"
            f"<br>Cake preferences: {cake_pref.cake_preference}"
            f"<br>Birthday: {emp.as_dict()['date_of_birth'].strftime('%B %d')}",
        }
    elif type(resp) == Dict or type(resp) == dict:
        cake_resp = {"baker_name": request.name, "cake_receiver": resp["message"]}
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
    return generate_show_cake_responsibility_template(cake_resp)
