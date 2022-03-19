from typing import Optional

from classic.components import component
from sqlalchemy import select, update
from classic.sql_storage import BaseRepository

from chat_app.application import interfaces
from chat_app.application.dataclasses import Chat, Message, User, ChatUser, UserShort
from . import tables


@component
class ChatsRepo(BaseRepository, interfaces.ChatsRepo):
    def get_by_id(self, chat_id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.chat_id == chat_id)
        # FIXME why scalars instead of scalar?
        return self.session.execute(query).scalars().one_or_none()

    def add(self, chat: Chat) -> Chat:
        self.session.add(chat)
        self.session.flush()
        self.session.refresh(chat)
        return chat

    def set_status(self, user_id: int, chat_id: int, status: str):
        query = update(ChatUser)\
            .where(ChatUser.user_id == user_id and ChatUser.chat_id == chat_id)\
            .values(status=status)
        self.session.execute(query)
        self.session.flush()
        self.session.commit()

    def delete(self, chat: Chat):
        self.session.delete(chat)
        self.session.flush()
        self.session.commit()

@component
class ChatUsersRepo(BaseRepository, interfaces.ChatUsersRepo):
    def add_participant(self, chat_user: ChatUser):
        self.session.add(chat_user)
        self.session.flush()

    def get_participant(self, chat_id: int, user_id: int):
        query = select(ChatUser).where(ChatUser.user_id == user_id, ChatUser.chat_id == chat_id)
        return self.session.execute(query).scalars().one_or_none()

    def get_all_participants(self, chat_id: int):
        # query = select(ChatUser).where(ChatUser.chat_id == chat_id)
        query = select([tables.chat_user.c.user_id]).where(tables.chat_user.c.chat_id == chat_id,
                                                           tables.chat_user.c.is_active == True).alias("id_list")
        query_users = select([tables.users.c.user_id, tables.users.c.username]).where(tables.users.c.user_id.in_(query))
        user_rows = self.session.execute(query_users).fetchall()

        return [UserShort(**dict(row)) for row in user_rows]


@component
class MessagesRepo(BaseRepository, interfaces.MessagesRepo):
    def add(self, message: Message):
        self.session.add(message)
        self.session.flush()
        self.session.commit()

    def get_chat_messages(self, chat_id: int):
        query = select(Message).where(Message.chat_id == chat_id)
        return self.session.execute(query).scalars().all()


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User:
        query = select(User).where(User.user_id == user_id)
        return self.session.execute(query).scalars().one_or_none()

