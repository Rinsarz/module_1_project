import datetime
from typing import List, Optional

import attr


@attr.dataclass
class User:
    username: str
    password: str
    email: str
    user_id: Optional[int] = None


@attr.dataclass
class Message:
    user_id: User
    chat_id: "Chat"
    message_text: str
    created: Optional[str] = attr.ib(
        factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    message_id: Optional[int] = None


@attr.dataclass
class Chat:
    creator_id: User
    info: str
    chat_id: Optional[int] = None


@attr.dataclass
class ChatUser:
    user_id: User
    chat_id: Chat
    is_active: bool
    changed: Optional[str] = attr.ib(
        factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    is_removed: bool = False

@attr.dataclass
class UserShort:
    user_id: int
    username: str