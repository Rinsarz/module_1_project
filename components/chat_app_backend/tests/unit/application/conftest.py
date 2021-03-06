from unittest.mock import Mock

import pytest

from chat_app.application import interfaces


@pytest.fixture(scope='function')
def chats_repo(chat_1):
    chats_repo = Mock(interfaces.ChatsRepo)
    chats_repo.get_by_id = Mock(return_value=chat_1)
    chats_repo.add = Mock(return_value=False)
    chats_repo.delete = Mock(return_value=None)
    return chats_repo


@pytest.fixture(scope='function')
def users_repo(user_1):
    users_repo = Mock(interfaces.UsersRepo)
    users_repo.get_by_id = Mock(return_value=user_1)
    users_repo.get_by_email = Mock(return_value=user_1)
    return users_repo


@pytest.fixture(scope='function')
def messages_repo(message_from_user_1_chat_1, message_from_user_2_chat_1):
    messages_repo = Mock(interfaces.MessagesRepo)
    messages_repo.get_chat_messages = Mock(return_value=[
        message_from_user_1_chat_1,
        message_from_user_2_chat_1
        ])
    messages_repo.add = Mock(return_value=False)

    return messages_repo


@pytest.fixture(scope='function')
def chat_users_repo(active_user_1_chat_1, active_user_2_chat_1, user_short_1):
    chat_users_repo = Mock(interfaces.ChatUsersRepo)
    chat_users_repo.get_participant = Mock(return_value=active_user_2_chat_1)
    chat_users_repo.add_participant = Mock(return_value=None)
    chat_users_repo.get_all_participants = Mock(return_value=[user_short_1])
    return chat_users_repo