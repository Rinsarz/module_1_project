from unittest.mock import Mock

import pytest
from chat_app.adapters import chat_api
from chat_app.application import services
from falcon import testing


@pytest.fixture(scope='function')
def users_service():
    service = Mock(services.Users)
    return service


@pytest.fixture(scope='function')
def chats_service():
    service = Mock(services.Chats)
    return service


@pytest.fixture(scope='function')
def client(chats_service, users_service):
    app = chat_api.create_app(
        is_dev_mode=True,
        allow_origins='*',
        chats=chats_service,
        users=users_service,
        )
    return testing.TestClient(app)