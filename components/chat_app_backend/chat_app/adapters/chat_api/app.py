import wsgiref.simple_server
from typing import Tuple, Union
import falcon


from classic.http_api import App
from chat_app.application import services
from . import controllers


def create_app(
    is_dev_mode: bool,
    allow_origins: Union[str, Tuple[str, ...]],
    chats: services.Chats,
    users: services.Users,
) -> App:

    app = App(prefix='/api')
    app.register(controllers.Users(users=users))
    app.register(controllers.Chats(chats=chats))

    return app



