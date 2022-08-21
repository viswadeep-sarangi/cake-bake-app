
from fastapi import APIRouter

from cake_bake_app.model import CakePreferencesModel
from cake_bake_app.model import CakePreferencesOrm

router = APIRouter()

@router.post("/submit_preferences", summary="Submitting cake preferences")
async def submit_preferences(request_body:CakePreferencesModel):
    cake_pref_orm = CakePreferencesOrm(**dict(request_body))
    """Submitting cake preferences"""
    print(request_body)
    print(cake_pref_orm)
    return {"message": "test"}


@router.get("/baking_responsibillity", summary="Getting cake baking responbilities")
async def get_cake_responsibility():
    """Getting cake baking responbilities"""
    return {"message":"test"}