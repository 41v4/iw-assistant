from fastapi import APIRouter

from app.api.chat_related import router as chat_history_router
from app.api.validation import router as validation_router
from app.views.home import router as home_router
from app.websockets.chat_ws import chat_websocket

main_router = APIRouter()

main_router.include_router(validation_router)
main_router.include_router(chat_history_router)
main_router.include_router(home_router)
main_router.add_websocket_route("/ws", chat_websocket)
