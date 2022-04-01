import datetime
from typing import Optional, List, Callable

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments

from chat_app.application.dataclasses import User, Chat, Message, \
    ChatUser, UserShort, ChatUserShort

from . import interfaces, errors

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    user_id: Optional[int]
    username: str
    password: str
    email: str


class UserInfoShort(DTO):
    user_id: int
    username: str

class UserInfoLogin(DTO):
    email: str
    password: str


class ChatInfo(DTO):
    chat_id: Optional[int]
    creator_id: int
    info: str


class ChatInfoUpdate(DTO):
    chat_id: int
    creator_id: Optional[int]
    info: Optional[str]
    user_id: int


class ChatInfoForLook(DTO):
    user_id: int
    chat_id: int


class MessageInfo(DTO):
    message_id: Optional[int] = None
    user_id: int
    chat_id: int
    message_text: str
    created: Optional[datetime.datetime] = None


class ChatUserInfo(DTO):
    user_id: int
    chat_id: int
    is_active: bool
    is_removed: bool


@component
class Chats:
    chats_repo: interfaces.ChatsRepo
    users_repo: interfaces.UsersRepo
    chat_users_repo: interfaces.ChatUsersRepo
    messages_repo: interfaces.MessagesRepo

    @staticmethod
    def _check_creator(chat: Chat, user_id: int):
        if not chat.creator_id == user_id:
            raise errors.NoPermission(user_id=user_id)

    def _check_participant(self, chat_id: int, user_id: int):
        self.get_participant(chat_id=chat_id, user_id=user_id)

    def _check_chat(self, chat_id: int):
        self.get_chat(chat_id=chat_id)


    def _add_chat_participant(self, chat_id: int, user_id: int, new_user_id: int):
        participant = self.chat_users_repo.get_participant(chat_id, new_user_id)

        if participant is not None and (not participant.is_active and not participant.is_removed):
            raise errors.NoPermission(user_id=user_id)

        if participant is not None:
            raise errors.AlreadyParticipant(user_id=new_user_id)

        chat_user_info = ChatUserInfo(
            user_id=new_user_id,
            chat_id=chat_id, is_active=True, is_removed=False
            )
        chat_user = chat_user_info.create_obj(ChatUser)
        self.chat_users_repo.add_participant(chat_user)

    @join_point
    @validate_with_dto
    def create_chat(self, chat_info: ChatInfo):

        new_chat = chat_info.create_obj(Chat)
        creator = self.users_repo.get_by_id(user_id=chat_info.creator_id)
        if creator is None:
            raise errors.NoUser(user_id=chat_info.creator_id)
        new_chat = self.chats_repo.add(chat=new_chat)

        chat_user_info = ChatUserInfo(user_id=creator.user_id,
                                      chat_id=new_chat.chat_id,
                                      is_active=True,
                                      is_removed=False)

        chat_user = chat_user_info.create_obj(ChatUser)
        self.chat_users_repo.add_participant(chat_user=chat_user)

    @join_point
    @validate_arguments
    def get_participant(self, chat_id: int, user_id: int) -> ChatUser:
        participant = self.chat_users_repo.get_participant(chat_id, user_id)
        if participant is None:
            raise errors.NoPermission(user_id=user_id)
        return participant

    @join_point
    @validate_arguments
    def get_chat(self, chat_id: int) -> Chat:
        chat = self.chats_repo.get_by_id(chat_id=chat_id)
        if not chat:
            raise errors.NoChat(chat_id=chat_id)
        return chat

    @join_point
    @validate_arguments
    def get_user(self, user_id: int) -> User:
        user = self.users_repo.get_by_id(user_id=user_id)
        if not user:
            raise errors.NoUser(user_id=user_id)
        return user

    @join_point
    @validate_arguments
    def add_participant(self, chat_id: int, user_id: int, new_user_id: int) -> ChatUserShort:
        chat = self.get_chat(chat_id=chat_id)
        self._check_creator(chat=chat, user_id=user_id)

        new_user = self.users_repo.get_by_id(user_id=new_user_id)
        if new_user is None:
            raise errors.NoUser(user_id=new_user_id)

        self._add_chat_participant(chat_id=chat_id, user_id=user_id, new_user_id=new_user_id)
        return ChatUserShort(user_id=new_user_id, chat_id=chat.chat_id)

    @join_point
    @validate_with_dto
    def update_chat_info(self, chat_info_update: ChatInfoUpdate):
        chat = self.get_chat(chat_id=chat_info_update.chat_id)
        self._check_creator(chat=chat, user_id=chat_info_update.user_id)
        delattr(chat_info_update, "user_id")
        chat_info_update.populate_obj(chat)

    @join_point
    @validate_arguments
    def delete_chat(self, chat_id: int, user_id: int):
        chat = self.get_chat(chat_id=chat_id)
        self._check_creator(chat=chat, user_id=user_id)
        self.chats_repo.delete(chat=chat)

    @join_point
    @validate_arguments
    def get_chat_info(self, chat_id: int, user_id: int) -> Chat:
        chat = self.get_chat(chat_id=chat_id)
        self._check_participant(chat_id=chat_id, user_id=user_id)
        return chat

    @join_point
    @validate_arguments
    def get_chat_participants(self, chat_id: int, user_id: int) -> List[UserShort]:
        self._check_chat(chat_id=chat_id)
        _ = self.get_user(user_id=user_id)

        self._check_participant(chat_id=chat_id, user_id=user_id)
        users = self.chat_users_repo.get_all_participants(chat_id=chat_id)
        return users

    @join_point
    @validate_arguments
    def remove_participant(self, chat_id: int, user_id: int, user_to_remove_id: int) -> ChatUserShort:
        chat = self.get_chat(chat_id=chat_id)

        self._check_creator(chat=chat, user_id=user_id)

        if user_id == user_to_remove_id:
            raise errors.NoPermission(user_id=user_id)

        user_to_remove = self.users_repo.get_by_id(user_to_remove_id)
        if not user_to_remove:
            raise errors.NoUser(user_id=user_to_remove_id)

        self._check_participant(chat_id=chat_id, user_id=user_to_remove_id)

        status = self.chat_users_repo.get_participant(chat_id=chat_id, user_id=user_to_remove_id)
        status.is_active = False
        status.is_removed = True

        return ChatUserShort(user_id=user_to_remove_id, chat_id=chat.chat_id)

    @join_point
    @validate_arguments
    def quit_chat(self, chat_id: int, user_id: int) -> ChatUserShort:
        chat = self.get_chat(chat_id)
        if chat.creator_id == user_id:
            self.chats_repo.delete(chat)
        else:
            user = self.users_repo.get_by_id(user_id)
            if user is None:
                raise errors.NoUser(user_id=user_id)

            self._check_participant(chat_id=chat_id, user_id=user_id)
            status = self.chat_users_repo.get_participant(chat_id=chat_id, user_id=user_id)
            status.is_active = False
            status.is_removed = False
        return ChatUserShort(user_id=user_id, chat_id=chat_id)

    @join_point
    @validate_with_dto
    def send_message(self, message_info: MessageInfo):
        user = self.users_repo.get_by_id(message_info.user_id)
        self._check_chat(message_info.chat_id)
        message = message_info.create_obj(Message)

        if not user:
            raise errors.NoUser(user_id=message_info.user_id)

        self._check_participant(chat_id=message_info.chat_id, user_id=message_info.user_id)
        self.messages_repo.add(message)

    @join_point
    @validate_arguments
    def get_messages(self, chat_id: int, user_id: int) -> List[Message]:
        chat = self.get_chat(chat_id)
        user = self.users_repo.get_by_id(user_id)
        if not user:
            raise errors.NoUser(user_id=user_id)

        self._check_creator(chat=chat, user_id=user_id)
        messages = self.messages_repo.get_chat_messages(chat_id)
        return messages


@component
class Users:
    users_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def register_user(self, user_info: UserInfo) -> UserShort:
        user = self.users_repo.get_by_email(email=user_info.email)
        if user is not None:
            raise errors.AlreadyRegistered(email=user_info.email)
        new_user = user_info.create_obj(User)
        new_user = self.users_repo.add(user=new_user)
        return UserShort(user_id=new_user.user_id,
                         username=new_user.username)

    @join_point
    @validate_arguments
    def get_user_by_id(self, user_id: int) -> User:
        user = self.users_repo.get_by_id(user_id)
        if user is None:
            raise errors.NoUser(user_id=user_id)
        return user

    @join_point
    @validate_arguments
    def login(self, email: str, password: str) -> UserShort:
        user = self.users_repo.get_by_email(email=email)
        if user is None or user.password != password:
            raise errors.NotRegistered()

        return UserShort(user_id=user.user_id, username=user.username)
