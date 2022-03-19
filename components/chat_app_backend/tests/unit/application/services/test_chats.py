import pytest
from pydantic import ValidationError
from chat_app.application.services import Chats
from chat_app.application.errors import NoPermission


@pytest.fixture(scope='function')
def service(chats_repo, messages_repo, chat_users_repo, users_repo):
    return Chats(
        chats_repo=chats_repo,
        messages_repo=messages_repo,
        chat_users_repo=chat_users_repo,
        users_repo=users_repo
        )


def test__check_creator(service, chat_1, user_1):
    result = service._check_creator(chat_1, user_id=user_1.user_id)
    assert result is None


def test__check_creator_error(service, chat_1, user_2):
    with pytest.raises(NoPermission):
        service._check_creator(chat_1, user_id=user_2.user_id)


def test__get_participant(service, chat_users_repo, active_user_2_chat_1):
    chat_id = active_user_2_chat_1.chat_id
    user_id = active_user_2_chat_1.user_id
    chat_users_repo.get_participant.return_value = active_user_2_chat_1

    result = service.get_participant(chat_id=chat_id, user_id=user_id)
    call_args, _ = chat_users_repo.get_participant.call_args

    assert call_args == (chat_id, user_id)
    assert result == active_user_2_chat_1


def test__check_participant_no_args(service, chat_users_repo):
    with pytest.raises(ValidationError):
        service._check_participant()


def test__add_participant(service, chats_repo, chat_users_repo):
    chat_id = 1
    user_id = 1
    new_user_id = 3

    chat_users_repo.get_participant.return_value = None
    service.add_participant(chat_id=chat_id, user_id=user_id, new_user_id=new_user_id)
    call_args, call_kwargs = chats_repo.get_by_id.call_args

    assert call_kwargs == {'chat_id': chat_id}


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

    call_args, call_kwargs = chats_repo.get_by_id.call_args

    assert call_kwargs == {'chat_id': chat_id}


def test__update_chat_info_no_args(service, chats_repo):
    user_id = 1
    creator_id = 1
    chat_info = 'new info'

    with pytest.raises(ValidationError):
        service.update_chat_info(
            user_id=user_id,
            creator_id=creator_id,
            info=chat_info)