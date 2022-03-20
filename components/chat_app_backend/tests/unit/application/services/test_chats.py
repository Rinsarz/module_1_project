from unittest.mock import Mock

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


def test__create_chat_no_args(service):
    with pytest.raises(ValidationError):
        service.create_chat()


def test__create_chat(service,
                      users_repo, chats_repo, chat_users_repo,
                      chat_1, user_1, active_user_1_chat_1):
    users_repo.get_by_id.return_value = user_1
    chats_repo.add.return_value = chat_1
    service.create_chat(chat_id=None,
                        creator_id=chat_1.creator_id,
                        info=chat_1.info)

    _, call_kwargs_1 = users_repo.get_by_id.call_args
    _, call_kwargs_2 = chats_repo.add.call_args
    _, call_kwargs_3 = chat_users_repo.add_participant.call_args

    new_chat = call_kwargs_2['chat']
    assert call_kwargs_1 == {'user_id': chat_1.creator_id}
    assert new_chat.creator_id == chat_1.creator_id
    assert new_chat.info == chat_1.info
    assert call_kwargs_3 == {'chat_user': active_user_1_chat_1}


def test__get_chat_no_args(service):
    with pytest.raises(ValidationError):
        service.get_chat()


def test__get_chat_args(service, chats_repo):
    chat_id = 1
    service.get_chat(chat_id)
    _, call_kwargs = chats_repo.get_by_id.call_args
    assert {'chat_id': chat_id} == call_kwargs


def test__get_chat_return(service, chats_repo, chat_1):
    chat = service.get_chat(chat_1.chat_id)
    chats_repo.get_by_id.return_value = chat_1
    assert chat == chat_1


def test__get_user_no_args(service):
    with pytest.raises(ValidationError):
        service.get_user()


def test__get_user_args(service, users_repo):
    user_id = 1
    service.get_user(user_id)
    _, call_kwargs = users_repo.get_by_id.call_args
    assert {'user_id': user_id} == call_kwargs


def test__get_user_return(service, users_repo, user_1):
    user = service.get_user(user_1.user_id)
    users_repo.get_by_id.return_value = user_1
    assert user == user_1


def test__delete_chat_no_args(service):
    with pytest.raises(ValidationError):
        service.delete_chat()


def test__delete_chat_args(service, chats_repo, chat_1):
    user_id = 1
    chat_id = 1
    service.get_chat = Mock(return_value=chat_1)
    service._check_creator = Mock(return_value=None)
    service.delete_chat(chat_id=chat_id, user_id=user_id)
    _, call_kwargs = chats_repo.delete.call_args
    assert {'chat': chat_1} == call_kwargs


def test__get_chat_info_no_args(service):
    service.get_chat = Mock(return_value=None)
    service._check_participant = Mock(return_value=None)
    with pytest.raises(ValidationError):
        service.get_chat_info()


def test__get_chat_info_args(service, chat_1):
    service.get_chat = Mock(return_value=chat_1)
    service._check_participant = Mock(return_value=None)
    _ = service.get_chat_info(
        chat_id=chat_1.chat_id,
        user_id=chat_1.creator_id)
    _, kwargs_1 = service.get_chat.call_args
    _, kwargs_2 = service._check_participant.call_args
    assert kwargs_1 == {'chat_id': chat_1.chat_id}
    assert kwargs_2 == {'chat_id': chat_1.chat_id, 'user_id': chat_1.creator_id}


def test__get_chat_info_return(service, chat_1):
    service.get_chat = Mock(return_value=chat_1)
    service._check_participant = Mock(return_value=None)
    result = service.get_chat_info(
        chat_id=chat_1.chat_id,
        user_id=chat_1.creator_id)
    assert chat_1 == result


def test__get_chat_participants_no_args(service):
    service._check_chat = Mock(result_value=None)
    service.get_user = Mock(return_value=None)
    service._check_participant = Mock(return_value=None)

    with pytest.raises(ValidationError):
        service.get_chat_participants()


def test__get_chat_participants_args(service, chat_1):
    service._check_chat = Mock(result_value=None)
    service.get_user = Mock(return_value=None)
    service._check_participant = Mock(return_value=None)
    service.get_chat_participants(chat_id=chat_1.chat_id, user_id=chat_1.creator_id)
    _, kwargs_1 = service._check_chat.call_args
    _, kwargs_2 = service.get_user.call_args
    _, kwargs_3 = service._check_participant.call_args

    assert {'chat_id': chat_1.chat_id} == kwargs_1
    assert {'user_id': chat_1.creator_id} == kwargs_2
    assert {'chat_id': chat_1.chat_id, 'user_id': chat_1.creator_id} == kwargs_3


def test__get_chat_participants_return(service, chat_1, user_short_1):
    service._check_chat = Mock(result_value=None)
    service.get_user = Mock(return_value=None)
    service._check_participant = Mock(return_value=None)
    result = service.get_chat_participants(chat_id=chat_1.chat_id, user_id=chat_1.creator_id)

    assert result == [user_short_1]


def test__get_remove_participant_no_args(service, user_1):
    service.get_chat = Mock(return_value=None)
    service._check_creator = Mock(return_value=None)
    service._check_participant = Mock(return_value=None)

    with pytest.raises(ValidationError):
        service.remove_participant()


def test__get_remove_participant_return(service, chat_users_repo,
                                        chat_1, user_1, user_2,
                                        active_user_2_chat_1, chat_user_short):
    service.get_chat = Mock(return_value=chat_1)
    service._check_creator = Mock(return_value=None)
    service._check_participant = Mock(return_value=None)
    result = service.remove_participant(
        chat_id=chat_1.chat_id,
        user_id=chat_1.creator_id,
        user_to_remove_id=user_2.user_id)

    assert result == chat_user_short


def test__get_remove_participant_no_permission(service, chat_users_repo,
                                               chat_1, user_1, user_2,
                                               active_user_2_chat_1, chat_user_short):
    service.get_chat = Mock(return_value=chat_1)
    service._check_creator = Mock(return_value=None)
    service._check_participant = Mock(return_value=None)

    with pytest.raises(NoPermission):
        _ = service.remove_participant(
            chat_id=chat_1.chat_id,
            user_id=chat_1.creator_id,
            user_to_remove_id=chat_1.creator_id)


def test__quit_chat(service):
    service.get_chat = Mock()
    service.is_creator = Mock(return_value=True)

    with pytest.raises(ValidationError):
        service.quit_chat()


def test__send_message(service):
    service._check_chat = Mock()
    service._check_participant = Mock()

    with pytest.raises(ValidationError):
        service.send_message()


def test__get_messages(service):
    service.get_chat = Mock()
    service._check_creator = Mock()

    with pytest.raises(ValidationError):
        service.get_messages()


def test__get_messages_return(service, chat_1, messages_repo):
    service.get_chat = Mock()
    service._check_creator = Mock()

    result = service.get_messages(chat_id=chat_1.chat_id,
                                  user_id=chat_1.creator_id)
    assert result == messages_repo.get_chat_messages()