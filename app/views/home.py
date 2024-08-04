from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.config import settings, templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home_view(request: Request):
    swagger_url = request.url_for("swagger_ui_html")
    return templates.TemplateResponse(
        "pages/chat.html",
        {"request": request, "app_name": settings.app_name, "swagger_url": swagger_url},
    )
