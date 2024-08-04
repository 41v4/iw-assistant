from fastapi import APIRouter, Request

from app.services.chat_session_manager import chat_session_manager

router = APIRouter(tags=["Chat-related"])


@router.get(
    "/api/get-chat-history",
    description="A basic API endpoint to check the chat history of a specific user token. The user token can be found at the bottom right side of the homepage.",
)
async def get_chat_history(request: Request, chat_token: str):
    chat_history = chat_session_manager.get_session_history(
        token=chat_token, max_msg_history_len=0
    )
    return {"chat_history": chat_history}
