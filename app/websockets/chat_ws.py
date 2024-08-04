import json
from typing import Dict

from fastapi import WebSocket, WebSocketDisconnect

from app.core.logger import logger
from app.models.chat import WSChatMessage
from app.services.chat_service import ChatService
from app.services.chat_session_manager import chat_session_manager


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def register(self, websocket: WebSocket, token: str):
        self.active_connections[token] = websocket

    def disconnect(self, token: str):
        self.active_connections.pop(token, None)
        chat_session_manager.remove_session(token)

    async def send_message(self, message: WSChatMessage, token: str):
        if websocket := self.active_connections.get(token):
            await websocket.send_json(message.dict())


manager = ConnectionManager()


async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    token = None
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "auth":
                token = await handle_auth(websocket, message)
                if not token:
                    break
            elif token and message.get("type") == "message":
                try:
                    max_msg_history_len = int(message.get("max_msg_history_len"))
                except ValueError:
                    max_msg_history_len = 0  # 0 means no length limitation
                chatting_settings = {"max_msg_history_len": max_msg_history_len}
                await handle_chat_message(websocket, token, message, chatting_settings)
            else:
                await websocket.send_json(
                    WSChatMessage(
                        type="error", content="Invalid message or not authenticated"
                    ).dict()
                )

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for {token}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        if token:
            manager.disconnect(token)
        logger.info(f"WebSocket connection closed for {token}")


async def handle_auth(websocket: WebSocket, message: dict) -> str:
    token = message.get("token")
    if token:
        await manager.register(websocket, token)
        logger.info(f"Authenticated user with token: {token}")
        await websocket.send_json(WSChatMessage(type="auth", content="success").dict())
        return token
    else:
        await websocket.send_json(WSChatMessage(type="auth", content="failed").dict())
        await websocket.close(code=1008, reason="Invalid token")
        return ""


async def handle_chat_message(
    websocket: WebSocket, token: str, message: dict, chatting_settings: dict
):
    user_message = message.get("message")
    logger.info(f"Received message from {token}: {user_message}")

    try:
        async for chunk in ChatService.generate_response(
            user_message, token, chatting_settings
        ):
            await manager.send_message(
                WSChatMessage(type="stream", content=chunk), token
            )
        await manager.send_message(WSChatMessage(type="end", content=""), token)
    except Exception as e:
        logger.error(f"Error in chat streaming for {token}: {str(e)}")
        await manager.send_message(
            WSChatMessage(type="error", content=f"An error occurred: {str(e)}"), token
        )
