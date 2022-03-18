import datetime
from typing import Optional, List

from classic.components import component
from classic.aspects import PointCut
from pydantic import validate_arguments

from chat_app.application.dataclasses import User, Chat, Message
from classic.app import DTO, validate_with_dto
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
    creator: int
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


@component
class Chats:
    chats_repo: interfaces.ChatsRepo
    users_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def create_chat(self, chat_info: ChatInfo):

        new_chat = chat_info.create_obj(Chat)
        creator = self.users_repo.get_by_id(chat_info.creator)
        if creator is None:
            raise errors.NoUser(user_id=chat_info.creator)
        new_chat.creator = creator
        new_chat.users.append(creator)
        self.chats_repo.add(new_chat)


    @join_point
    @validate_arguments
    def add_participant(self, chat_id: int, user_id: int, new_user_id: int) -> ChatInfoForLook:
        chat = self.chats_repo.get_by_id(chat_id)
        if not chat.is_creator(user_id):
            raise errors.NoPermission(user_id=user_id)
        if not chat:
            raise errors.NoChat(chat_id=chat_id)
        new_user = self.users_repo.get_by_id(new_user_id)
        if new_user is None:
            raise errors.NoUser(user_id=new_user_id)
        chat.add_participant(new_user)
        return ChatInfoForLook.parse_obj({"user_id": new_user_id, "chat_id": chat.chat_id})

            # chat.set_status(user_to_remove_id, chat_id, 'removed')
    @join_point
    @validate_arguments
    def set_status(self, user_id: int, chat_id: int, status: str):
        self.chats_repo.set_status(user_id, chat_id, status)

    def update_chat_info(self, chat_info: ChatInfo, user_id: int):
        chat = self.chats_repo.get_by_id(chat_info.chat_id)
        if not chat.is_creator(user_id):
            # TODO how check admin permission?
            return
        if chat is None:
            raise errors.NoChat(chat_id=chat_info.chat_id)

    @validate_arguments
    def delete_chat(self, chat_id: int, user_id: int):
        chat = self.chats_repo.get_by_id(chat_id)
        if not chat.is_creator(user_id):
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

        if user not in chat.users:
            raise errors.NoPermission(user_id=user_id)

        return chat

    @validate_arguments
    def get_users_list(self, chat_id: int, user_id: int) -> Optional[List[User]]:
        chat = self.chats_repo.get_by_id(chat_id)
        user = self.users_repo.get_by_id(user_id)
        if not chat:
            raise errors.NoChat(chat_id=chat_id)
        if not user:
            raise errors.NoUser(chat_id=chat_id)
        if user not in chat.users:
            # TODO how check participant permission?
            return
        return chat.users

    @join_point
    @validate_arguments
    def remove_participant(self, chat_id: int, user_id: int, user_to_remove_id: int) -> ChatInfoForLook:
        chat = self.chats_repo.get_by_id(chat_id)
        if not chat:
            raise errors.NoChat(chat_id=chat_id)

        if not chat.is_creator(user_id):
            raise errors.NoPermission(user_id=user_id)

        if user_id == user_to_remove_id:
            raise errors.NoPermission(user_id=user_id)

        user_to_remove = self.users_repo.get_by_id(user_to_remove_id)
        if not user_to_remove:
            raise errors.NoUser(user_id=user_to_remove_id)

        if not chat.is_participant(user_to_remove):
            raise errors.NoParticipant(user_id=user_to_remove_id)

        chat.remove_participant(user_to_remove)
        self.chats_repo.set_status(user_to_remove_id, chat_id, 'removed')
        return ChatInfoForLook.parse_obj({"user_id": user_to_remove_id, "chat_id": chat.chat_id})

    @validate_arguments
    def quit_chat(self, chat_id: int, user_id: int) -> ChatInfoForLook:
        chat = self.chats_repo.get_by_id(chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_id)
        if chat.is_creator(user_id):
            self.chats_repo.delete(chat)
        else:
            user = self.users_repo.get_by_id(user_id)
            if user is None:
                raise errors.NoUser(user_id=user_id)
            chat.remove_participant(user)
        return ChatInfoForLook.parse_obj({"user_id": user_id, "chat_id": chat_id})

    @validate_with_dto
    def send_message(self, message_info: MessageInfo):
        user = self.users_repo.get_by_id(message_info.user_id)
        chat = self.chats_repo.get_by_id(message_info.chat_id)
        message = message_info.create_obj(Message)

        if chat is None:
            raise errors.NoChat(chat_id=message_info.chat_id)

        if not user:
            raise errors.NoUser(chat_id=message_info.chat_id)

        if user not in chat.users:
            # TODO how check participant permission?
            return

        chat.add_message(message)

    @validate_arguments
    def get_messages(self, chat_id: int, user_id: int) -> List[Message]:
        user = self.users_repo.get_by_id(user_id)
        chat = self.chats_repo.get_by_id(chat_id)

        if chat is None:
            raise errors.NoChat(chat_id=chat_id)

        if not user:
            raise errors.NoUser(chat_id=chat_id)

        if not chat.is_creator(user_id):
            # TODO how check admin permission?
            raise errors.NoPermission(user_id=user_id)

        return chat.messages


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