from abc import ABC, abstractmethod
from .dataclasses import Chat, Message, User, Status


class ChatsRepo(ABC):
    @abstractmethod
    def add(self, chat: Chat):
        ...

    @abstractmethod
    def get_by_id(self, _id: int) -> Chat:
        ...

    @abstractmethod
    def delete(self, chat: Chat):
        ...

    def set_status(self, chat_id: int, user_id: int, status: str):
        ...


class MessagesRepo(ABC):
    @abstractmethod
    def add(self, message: Message):
        ...


class UsersRepo:
    @abstractmethod
    def add(self, user: User):
        ...

    @abstractmethod
    def get_by_id(self, _id: int) -> User:
        ...


class StatusesRepo:
    @abstractmethod
    def add(self, status: Status):
        ...