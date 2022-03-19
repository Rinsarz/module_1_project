import pytest
from chat_app.application.services import Chats


@pytest.fixture(scope='function')
def service(chats_repo, messages_repo, chat_users_repo, users_repo):
    return Chats(
        chats_repo=chats_repo,
        messages_repo=messages_repo,
        chat_users_repo=chat_users_repo,
        users_repo=users_repo
        )


def test__is_participant(service, chat_users_repo):
    chat_id = 1
    user_id = 1

    service.is_participant(chat_id=chat_id, user_id=user_id)
    call_args, _ = chat_users_repo.get_participant.call_args

    assert call_args == (chat_id, user_id)