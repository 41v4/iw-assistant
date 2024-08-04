from pydantic import BaseModel


class WSChatMessage(BaseModel):
    type: str
    content: str
