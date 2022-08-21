from typing import Dict
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from cake_bake_app.template import generate_test_html_response

router = APIRouter()


@router.get("/test", summary="HTML test endpoint", response_class=HTMLResponse)
async def test() -> HTMLResponse:
    return generate_test_html_response()



