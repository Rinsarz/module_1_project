import pytest
from pydantic import ValidationError

from chat_app.application import errors
from chat_app.application.services import Users


@pytest.fixture(scope='function')
def service(chats_repo, messages_repo, chat_users_repo, users_repo):
    return Users(
        users_repo=users_repo
        )


def test__register_user_no_args(service):
    with pytest.raises(ValidationError):
        service.register_user()


def test__register_user_registered(service):
    username = 'my_username'
    password = 'pass123'
    email = 'test@test.com'
    with pytest.raises(errors.AlreadyRegistered):
        service.register_user(username=username, password=password, email=email)


def test__get_user_by_id_no_args(service):
    with pytest.raises(ValidationError):
        service.register_user()


def test__login_no_args(service):
    with pytest.raises(ValidationError):
        service.register_user()