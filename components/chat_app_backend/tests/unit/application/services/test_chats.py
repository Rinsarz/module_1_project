import pytest
from pydantic import ValidationError
from chat_app.application.services import Chats


@pytest.fixture(scope='function')
def service(chats_repo, messages_repo, chat_users_repo, users_repo):
    return Chats(
        chats_repo=chats_repo,
        messages_repo=messages_repo,
        chat_users_repo=chat_users_repo,
        users_repo=users_repo
        )


def test__is_creator(service, chat_1, user_1):
    assert service.is_creator(chat_1, user_id=user_1.user_id)


def test__is_participant(service, chat_users_repo):
    chat_id = 1
    user_id = 1

    result = service.is_participant(chat_id=chat_id, user_id=user_id)
    call_args, _ = chat_users_repo.get_participant.call_args

    assert call_args == (chat_id, user_id)
    assert result == True


def test__is_participant_no_args(service, chat_users_repo):
    with pytest.raises(ValidationError):
        service.is_participant()


def test__add_participant(service, chats_repo):
    chat_id = 1
    user_id = 1
    new_user_id = 2
    service.add_participant(chat_id=chat_id, user_id=user_id, new_user_id=new_user_id)
    call_args, _ = chats_repo.get_by_id.call_args

    assert call_args == (chat_id,)


def test__update_chat_info(service, chats_repo):
    user_id = 1
    creator_id = 1
    chat_id = 1
    chat_info = 'new info'

    service.update_chat_info(
        user_id=user_id,
        creator_id=creator_id,
        chat_id=chat_id,
        info=chat_info)

    call_args, _ = chats_repo.get_by_id.call_args

    assert call_args == (chat_id,)


def test__update_chat_info_no_args(service, chats_repo):
    user_id = 1
    creator_id = 1
    chat_info = 'new info'

    with pytest.raises(ValidationError):
        service.update_chat_info(
            user_id=user_id,
            creator_id=creator_id,
            info=chat_info)
