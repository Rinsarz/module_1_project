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
    message_id: int
    user: User
    message_text: str
    created: Optional[str] = attr.ib(
        factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@attr.dataclass
class Chat:
    creator_id: User
    info: str
    users: List[User] = attr.ib(factory=list)
    messages: List[Message] = attr.ib(factory=list)
    chat_id: Optional[int] = None

    def add_participant(self, user: User):
        if user not in self.users:
            self.users.append(user)

    def remove_participant(self, user: User):
        # TODO Change to try except?
        if user in self.users:
            self.users.remove(user)

    def is_creator(self, user_id: int):
        if self.creator_id.user_id == user_id:
            return True
        return False

    def is_participant(self, user: User):
        if user in self.users:
            return True
        return False

    def add_message(self, message: Message):
        self.messages.append(message)


@attr.dataclass
class Status:
    status_id: int
    status_name: str


@attr.dataclass
class ChatUser:
    user: User
    chat: Chat
    changed:  Optional[str] = attr.ib(
        factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # FIXME how make datetime?
    status: Optional[Status] = None
