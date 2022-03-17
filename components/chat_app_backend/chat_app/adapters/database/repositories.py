from typing import Optional

from classic.components import component
from sqlalchemy import select
from classic.sql_storage import BaseRepository

from chat_app.application import interfaces
from chat_app.application.dataclasses import Chat, Message, User, Status

@component
class ChatsRepo(BaseRepository, interfaces.ChatsRepo):
    def get_by_id(self, _id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.chat_id == _id)
        # FIXME why scalars instead of scalar?
        return self.session.execute(query).scalars().one_or_none()

    def add(self, chat: Chat):
        self.session.add(chat)
        self.session.flush()
        self.session.commit()

    def delete(self, chat: Chat):
        self.session.delete(chat)

@component
class MessagesRepo(BaseRepository, interfaces.MessagesRepo):
    def add(self, message: Message):
        self.session.add(message)
        self.session.flush()
        self.session.commit()

@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def add(self, user: User):
        self.session.add(user)
        self.session.flush()
        self.session.commit()

    def get_by_id(self, _id: int) -> User:
        query = select(User).where(User.user_id == _id)
        return self.session.execute(query).scalars().one_or_none()

@component
class StatusesRepo(BaseRepository, interfaces.StatusesRepo):
    def add(self, status: Status):
        self.session.add(status)
        self.session.flush()

