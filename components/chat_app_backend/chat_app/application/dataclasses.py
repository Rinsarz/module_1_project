import attr


@attr.dataclass
class Chat:
    chat_id: int
    creator: User
    users: List[User] = attr.ib(factory=list)
    messages: List[Message] = attr.ib(factory=list)


@attr.dataclass
class User:
    user_id: int
    username: str
    password: str
    email: str


@attr.dataclass
class Message:
    message_id: int
    user: User
    created: datetime.datetime


@attr.dataclass
class Status:
    status_id: int
    status_name: str


@attr.dataclass
class ChatUser:
    user: User
    chat: Chat
    status: Status
    changed: datetime.datetime