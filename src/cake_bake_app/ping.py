from typing import Dict
from fastapi import APIRouter
from fastapi.requests import Request
from cake_bake_app.models import Employees, EmployeesModel
router = APIRouter()


@router.get("/", summary="Test endpoint")
async def test() -> Dict[str, str]:
    """Test endpoint for retuning a ping."""
    return {"Application": "Cake Bake App"}

@router.post("/form", summary="Test endpoint for form")
async def test_form(request:EmployeesModel):
    """Test endpoint for submitting a form"""
    # _json = await request.json()
    print(request)
    _dict = dict(request)
    return {"json":_dict}
