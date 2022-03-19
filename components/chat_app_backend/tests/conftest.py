import datetime

import pytest as pytest

from chat_app.application import dataclasses


@pytest.fixture
def chat_1(user_1, user_2):
    return dataclasses.Chat(
        chat_id=1,
        creator_id=user_1,
        info='test chat',
        )


@pytest.fixture
def chat_2(user_2):
    return dataclasses.Chat(
        chat_id=1,
        creator_id=user_2,
        info='test chat',
        )


@pytest.fixture
def user_1():
    return dataclasses.User(
        user_id=1,
        username='Ivanov',
        password='test_pass',
        email='ivanov@test.ru'
        )


@pytest.fixture
def user_2():
    return dataclasses.User(
        user_id=2,
        username='Petrov',
        password='test_pass',
        email='petrov@test.ru'
        )


@pytest.fixture
def date_string_1():
    return "12/11/2018 09:15:32"


@pytest.fixture
def date_string_2():
    return "23/12/2019 10:34:21"


@pytest.fixture
def message_from_user_1_chat_1(user_1, chat_1, date_string_1):
    return dataclasses.Message(
        message_id=1,
        user_id=user_1,
        chat_id=chat_1,
        created=datetime.datetime.strptime(date_string_1, "%d/%m/%Y %H:%M:%S"),
        message_text='Message 1 text'
        )


@pytest.fixture
def message_from_user_2_chat_1(user_2, chat_1, date_string_2):
    return dataclasses.Message(
        message_id=2,
        user_id=user_2,
        chat_id=chat_1,
        created=datetime.datetime.strptime(date_string_2, "%d/%m/%Y %H:%M:%S"),
        message_text='Message 2 text'
        )


@pytest.fixture
def active_user_1_chat_1(user_1, chat_1):
    return dataclasses.ChatUser(
        user_id=user_1,
        chat_id=chat_1,
        is_active=True,
        is_removed=False
        )


@pytest.fixture
def active_user_2_chat_1(user_2, chat_1):
    return dataclasses.ChatUser(
        user_id=user_2,
        chat_id=chat_1,
        is_active=True,
        is_removed=False
        )