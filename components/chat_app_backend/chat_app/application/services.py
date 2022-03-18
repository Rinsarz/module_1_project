import datetime
from typing import Optional, List

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments

from chat_app.application.dataclasses import User, Chat, Message, ChatUser, UserShort
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


class ChatInfo(DTO):
    chat_id: Optional[int]
    creator_id: int
    info: str


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
    chat_user_repo: interfaces.ChatUsersRepo
    messages_repo: interfaces.MessagesRepo

    @join_point
    @validate_with_dto
    def create_chat(self, chat_info: ChatInfo):

        new_chat = chat_info.create_obj(Chat)
        creator = self.users_repo.get_by_id(chat_info.creator_id)
        if creator is None:
            raise errors.NoUser(user_id=chat_info.creator_id)
        new_chat = self.chats_repo.add(new_chat)

        chat_user_info = ChatUserInfo(user_id=creator.user_id,
                                      chat_id=new_chat.chat_id,
                                      is_active=True,
                                      is_removed=False)

        chat_user = chat_user_info.create_obj(ChatUser)
        self.chat_user_repo.add_participant(chat_user)

    @staticmethod
    def is_creator(chat: Chat, user_id: int):
        return chat.creator_id == user_id

    @validate_arguments
    def is_participant(self, chat_id: int, user_id: int):
        participant = self.chat_user_repo.get_participant(chat_id, user_id)
        if participant is not None:
            return True
        return False

    @join_point
    @validate_arguments
    def add_participant(self, chat_id: int, user_id: int, new_user_id: int) -> ChatInfoForLook:
        chat = self.chats_repo.get_by_id(chat_id)

        if not self.is_creator(chat, user_id):
            raise errors.NoPermission(user_id=user_id)
        if not chat:
            raise errors.NoChat(chat_id=chat_id)

        new_user = self.users_repo.get_by_id(new_user_id)

        if new_user is None:
            raise errors.NoUser(user_id=new_user_id)

        chat_user = self.chat_user_repo.get_participant(chat_id, new_user_id)

        if chat_user is not None and (not chat_user.is_active and not chat_user.is_removed):
            raise errors.NoPermission(user_id=user_id)

        chat_user_info = ChatUserInfo(
            user_id=new_user.user_id,
            chat_id=chat.chat_id, is_active=True, is_removed=False
            )
        chat_user = chat_user_info.create_obj(ChatUser)
        self.chat_user_repo.add_participant(chat_user)
        return ChatInfoForLook.parse_obj({'user_id': new_user_id, 'chat_id': chat.chat_id})

    def update_chat_info(self, chat_info: ChatInfo, user_id: int):
        chat = self.chats_repo.get_by_id(chat_info.chat_id)
        if not self.is_creator(user_id):
            # TODO how check admin permission?
            return
        if chat is None:
            raise errors.NoChat(chat_id=chat_info.chat_id)

    @validate_arguments
    def delete_chat(self, chat_id: int, user_id: int):
        chat = self.chats_repo.get_by_id(chat_id)
        if not self.is_creator(chat, user_id):
            raise errors.NoPermission(user_id=user_id)
        self.chats_repo.delete(chat)

    @validate_arguments
    def get_chat_info(self, chat_id: int, user_id: int) -> Chat:
        chat = self.chats_repo.get_by_id(chat_id)
        user = self.users_repo.get_by_id(user_id)

        if not chat:
            raise errors.NoChat(chat_id=chat_id)
        if not user:
            raise errors.NoUser(chat_id=chat_id)

        if not self.is_participant(chat_id, user_id):
            raise errors.NoPermission(user_id=user_id)

        return chat

    @validate_arguments
    def get_chat_participants(self, chat_id: int, user_id: int) -> List[UserShort]:
        chat = self.chats_repo.get_by_id(chat_id)
        user = self.users_repo.get_by_id(user_id)

        if not chat:
            raise errors.NoChat(chat_id=chat_id)
        if not user:
            raise errors.NoUser(chat_id=chat_id)

        if not self.is_participant(chat_id, user_id):
            raise errors.NoPermission(user_id=user_id)

        users = self.chat_user_repo.get_all_participants(chat_id)
        return users

    @join_point
    @validate_arguments
    def remove_participant(self, chat_id: int, user_id: int, user_to_remove_id: int) -> ChatInfoForLook:
        chat = self.chats_repo.get_by_id(chat_id)
        if not chat:
            raise errors.NoChat(chat_id=chat_id)

        if not self.is_creator(chat, user_id):
            raise errors.NoPermission(user_id=user_id)

        if user_id == user_to_remove_id:
            raise errors.NoPermission(user_id=user_id)

        user_to_remove = self.users_repo.get_by_id(user_to_remove_id)
        if not user_to_remove:
            raise errors.NoUser(user_id=user_to_remove_id)

        if not self.is_participant(chat_id, user_id):
            raise errors.NoParticipant(user_id=user_to_remove_id)

        status = self.chat_user_repo.get_participant(chat_id=chat_id, user_id=user_id)
        status.is_active = False
        status.is_removed = True

        return ChatInfoForLook.parse_obj({'user_id': user_to_remove_id, 'chat_id': chat.chat_id})

    @validate_arguments
    def quit_chat(self, chat_id: int, user_id: int) -> ChatInfoForLook:
        chat = self.chats_repo.get_by_id(chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_id)
        if self.is_creator(chat, user_id):
            self.chats_repo.delete(chat)
        else:
            user = self.users_repo.get_by_id(user_id)
            if user is None:
                raise errors.NoUser(user_id=user_id)

            status = self.chat_user_repo.get_participant(chat_id=chat_id, user_id=user_id)
            status.is_active = False
            status.is_removed = False
        return ChatInfoForLook.parse_obj({'user_id': user_id, 'chat_id': chat_id})

    @validate_with_dto
    def send_message(self, message_info: MessageInfo):
        user = self.users_repo.get_by_id(message_info.user_id)
        chat = self.chats_repo.get_by_id(message_info.chat_id)
        message = message_info.create_obj(Message)

        if chat is None:
            raise errors.NoChat(chat_id=message_info.chat_id)

        if not user:
            raise errors.NoUser(chat_id=message_info.chat_id)

        if not self.is_participant(chat.chat_id, user.user_id):
            # TODO how check participant permission?
            return

        self.messages_repo.add(message)

    @validate_arguments
    def get_messages(self, chat_id: int, user_id: int) -> List[Message]:
        user = self.users_repo.get_by_id(user_id)
        chat = self.chats_repo.get_by_id(chat_id)

        if chat is None:
            raise errors.NoChat(chat_id=chat_id)

        if not user:
            raise errors.NoUser(chat_id=chat_id)

        if not self.is_creator(chat, user_id):
            # TODO how check admin permission?
            raise errors.NoPermission(user_id=user_id)

        messages = self.messages_repo.get_chat_messages(chat_id)
        messages = list(messages)
        return messages


@component
class Users:
    users_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def register_user(self, user_info: UserInfo) -> UserInfoShort:
        new_user = user_info.create_obj(User)
        new_user = self.users_repo.add(new_user)
        return UserInfoShort.parse_obj({'user_id': new_user.user_id, 'username': new_user.username})

    @validate_arguments
    def get_user_by_id(self, user_id: int):
        user = self.users_repo.get_by_id(user_id)
        if user is None:
            raise errors.NoUser(user_id=user_id)
        return user

# class Messenger:
#     users_repo: interfaces.UsersRepo
#     chats_repo: interfaces.ChatsRepo