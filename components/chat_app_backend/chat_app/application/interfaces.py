from abc import ABC, abstractmethod
from .dataclasses import Chat, Message, User, ChatUser


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


class ChatUsersRepo(ABC):
    @abstractmethod
    def add_participant(self, chat_user: ChatUser):
        pass

    @abstractmethod
    def get_participant(self, chat_id: int, user_id: int):
        pass

    @abstractmethod
    def get_all_participants(self, chat_id: int):
        pass




class MessagesRepo(ABC):
    @abstractmethod
    def add(self, message: Message):
        ...

    @abstractmethod
    def get_chat_messages(self, chat_id: int):
        pass


class UsersRepo:
    @abstractmethod
    def add(self, user: User):
        ...

    @abstractmethod
    def get_by_id(self, _id: int) -> User:
        ...

