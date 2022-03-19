import os
from typing import Tuple, Union
from classic.http_auth import Authenticator, strategies

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

    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)

    authenticator.set_strategies(strategies.JWT(secret_key=os.getenv('JWT_SECRET')))

    app = App(prefix='/api')
    app.register(controllers.Users(users=users))
    app.register(controllers.Chats(authenticator=authenticator, chats=chats))

    return app



