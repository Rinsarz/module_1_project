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
    user_id: int
    chat_id: int
    message_text: str
    created: Optional[datetime.datetime] = attr.ib(
        factory=lambda: datetime.datetime.utcnow())
    message_id: Optional[int] = None


@attr.dataclass
class Chat:
    creator_id: int
    info: str
    chat_id: Optional[int] = None


@attr.dataclass
class ChatUser:
    user_id: int
    chat_id: int
    is_active: bool
    changed: Optional[datetime.datetime] = attr.ib(
        factory=lambda: datetime.datetime.utcnow())
    is_removed: bool = False


@attr.dataclass
class ChatUserShort:
    user_id: int
    chat_id: int


@attr.dataclass
class UserShort:
    user_id: int
    username: str