from typing import Dict, List

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.messages import BaseMessage


def trim_messages(
    message_history: InMemoryChatMessageHistory,
    perm_msgs: List[BaseMessage],
    max_msg_history_len: int,
):
    for msg_obj in message_history.messages:
        if msg_obj not in perm_msgs:
            perm_msgs.append(msg_obj)

    message_history.clear()
    for message in perm_msgs[-max_msg_history_len:]:
        message_history.add_message(message)

    return message_history


class SessionManager:
    def __init__(self):
        self.active_chat_sessions: Dict[str, BaseChatMessageHistory] = {}
        self.active_chat_sessions_perm_msgs: Dict[str, BaseMessage] = {}

    def get_session_history(
        self, token: str, max_msg_history_len: int
    ) -> BaseChatMessageHistory:
        if token not in self.active_chat_sessions:
            self.active_chat_sessions[token] = (
                InMemoryChatMessageHistory()
            )  # will be cleared and re-populated (due to the message trimming feature)
            self.active_chat_sessions_perm_msgs[
                token
            ] = []  # will contain all permanent messages
        trimmed_messages = trim_messages(
            message_history=self.active_chat_sessions[token],
            perm_msgs=self.active_chat_sessions_perm_msgs[token],
            max_msg_history_len=max_msg_history_len,
        )
        return trimmed_messages

    def remove_session(self, token: str):
        self.active_chat_sessions.pop(token, None)


chat_session_manager = SessionManager()
