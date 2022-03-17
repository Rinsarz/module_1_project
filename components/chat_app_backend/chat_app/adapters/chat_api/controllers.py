import falcon
from classic.components import component
from falcon import Request, Response

from chat_app.application import services
from .join_points import join_point

@component
class Users:
    users: services.Users


@component
class Chats:
    chats: services.Chats

    @join_point
    def on_get_show_messages(self, request: Request, response: Response):
        # user_id = int(request.headers['TOKEN'])
        messages = self.chats.get_messages(
            # user_id=user_id,
            **request.media)
        response.media = {
            'messages': [{
                'message_text': message.message_text,
                'message_author': message.user.username,
                'message_author_id': message.user.user_id,
                'message_created': message.created
                }
                for message in messages]
            }

    @join_point
    def on_post_add_chat(self, request: Request, response:Response):
        self.chats.create_chat(**request.media)

@component
class Users:
    users: services.Users

    @join_point
    def on_post_register(self, request: Request, response: Response):
        self.users.register_user(**request.media)
        response.media = {
            "message": "Account successfully created"
        }
        response.status = falcon.HTTP_201

    @join_point
    def on_get_user_info(self, request: Request, response: Response):
        user = self.users.get_user_by_id(**request.media)
        response.media = {
            "id": user.user_id,
            "username": user.username,
            "email": user.email
            }



