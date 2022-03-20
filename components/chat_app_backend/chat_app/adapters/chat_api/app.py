import os
from typing import Tuple, Union
from classic.http_auth import Authenticator, strategies
from chat_app.adapters.chat_api.auth import SimpleAuthenticator

from . import auth

from classic.http_api import App
from chat_app.application import services
from . import controllers


def create_app(
    is_dev_mode: bool,
    allow_origins: Union[str, Tuple[str, ...]],
    chats: services.Chats,
    users: services.Users,
) -> App:

    authenticator = SimpleAuthenticator(app_groups=auth.ALL_GROUPS)

    if is_dev_mode:
        authenticator.set_strategies(auth.test_strategy)
    else:
        authenticator.set_strategies(auth.jwt_id_strategy)
        # authenticator.set_strategies(auth.header_id_strategy)

    app = App(prefix='/api')
    app.register(controllers.Users(authenticator=authenticator, users=users))
    app.register(controllers.Chats(authenticator=authenticator, chats=chats))

    return app



