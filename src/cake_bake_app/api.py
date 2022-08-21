
from typing import Dict, List
from fastapi import APIRouter, Depends

from cake_bake_app.model import CakePreferencesModel
from cake_bake_app.model import CakePreferences
from cake_bake_app.db import add_cake_preference, all_cake_preferences, get_session

router = APIRouter()

@router.post("/submit_preferences", summary="Submit cake preferences")
async def submit_preferences(request_body:CakePreferencesModel, session=Depends(get_session)):
    cake_pref_orm = CakePreferences(**dict(request_body))
    """Submit cake preferences"""
    print(request_body)
    print(cake_pref_orm)
    cake_pref_orm = add_cake_preference(cake_preference=cake_pref_orm, session=session)
    return {"message": "test"}


@router.get("/preferences", summary="Get all cake baking responbilities")
async def get_all_cake_preferences(session=Depends(get_session))->List[Dict[str,str]]:
    """Get all cake baking responbilities"""
    all_cake_prefs = all_cake_preferences(session=session)
    return all_cake_prefs


@router.post("/baking_responsibillity", summary="Get cake baking responbilities")
async def get_cake_responsibility(name:str):
    """Get cake baking responbilities"""
    return {"message":"test"}