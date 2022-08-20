from typing import Dict
from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Test endpoint")
async def test() -> Dict[str, str]:
    """Test endpoint for retuning a ping."""
    return {"Application": "Cake Bake App"}
