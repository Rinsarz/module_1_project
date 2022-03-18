from typing import Optional

from classic.components import component
from sqlalchemy import select, update
from classic.sql_storage import BaseRepository

from chat_app.application import interfaces
from chat_app.application.dataclasses import Chat, Message, User, Status, ChatUser


@component
class ChatsRepo(BaseRepository, interfaces.ChatsRepo):
    def get_by_id(self, _id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.chat_id == _id)
        # FIXME why scalars instead of scalar?
        return self.session.execute(query).scalars().one_or_none()

    def add(self, chat: Chat) -> Chat:
        self.session.add(chat)
        self.session.flush() # FIXME flush commit how make it right?
        self.session.commit()
        self.session.refresh(chat)
        return chat

    def set_status(self, user_id: int, chat_id: int, status: str):
        query = update(ChatUser)\
            .where(ChatUser.user.user_id == user_id and ChatUser.chat.chat_id == chat_id)\
            .values(status=status)
        self.session.execute(query)
        self.session.flush()
        self.session.commit()

    def delete(self, chat: Chat):
        self.session.delete(chat)
        self.session.flush()
        self.session.commit()


@component
class MessagesRepo(BaseRepository, interfaces.MessagesRepo):
    def add(self, message: Message):
        self.session.add(message)
        self.session.flush()
        self.session.commit()


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, _id: int) -> User:
        query = select(User).where(User.user_id == _id)
        return self.session.execute(query).scalars().one_or_none()


@component
class StatusesRepo(BaseRepository, interfaces.StatusesRepo):
    def add(self, status: Status):
        self.session.add(status)
        self.session.flush()