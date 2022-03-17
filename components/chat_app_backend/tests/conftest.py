import datetime

import pytest as pytest

from chat_app.application import dataclasses


@pytest.fixture
def chat(user_1, user_2, message_1, message_2):
    return dataclasses.Chat(
        chat_id=1,
        creator=user_1,
        info='test chat',
        users=[user_1, user_2],
        messages=[message_1, message_2]
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
def message_1(user_1, date_string_1):
    return dataclasses.Message(
        message_id=1,
        user=user_1,
        created=datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S"),
        message_text='Message 1 text'
        )

@pytest.fixture
def message_2(user_2):
    return dataclasses.Message(
        message_id=2,
        user=user_2,
        created=datetime.datetime.now(),
        message_text='Message 2 text'
        )