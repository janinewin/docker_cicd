from typing import TypedDict


class Message(TypedDict):
    message: str
    received_at: str
    username: str
