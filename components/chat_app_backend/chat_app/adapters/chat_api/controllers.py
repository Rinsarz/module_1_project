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
        messages = self.chats.get_messages(
            **request.media)
        if len(messages) > 0:
            response.media = {
                'messages': [{
                    'message_id': message.message_id,
                    'message_text': message.message_text,
                    'message_author': message.user_id,
                    'message_author_id': message.user_id,
                    'message_created': message.created
                    }
                    for message in messages]
                }
            response.status = falcon.HTTP_404
        else:
            response.media = {
                'message': 'No messages in this chat yet'
                }

    @join_point
    def on_post_add_chat(self, request: Request, response: Response):
        self.chats.create_chat(**request.media)
        response.media = {
            'message': 'chat was successfully created'
            }
        response.status = falcon.HTTP_201

    @join_point
    def on_post_send_message(self, request: Request, response: Response):
        self.chats.send_message(**request.media)
        response.media = {
            'message': 'message was sent'
            }
        response.status = falcon.HTTP_200

    @join_point
    def on_get_chat_info(self, request: Request, response: Response):
        chat = self.chats.get_chat_info(**request.media)
        response.media = {
            'chat id': chat.chat_id,
            'chat info': chat.info,
            'chat creator id': chat.creator.user_id,
            'chat users:': [{user.user_id: user.username} for user in chat.users]
            }
        response.status = falcon.HTTP_200

    @join_point
    def on_post_add_participant(self, request: Request, response: Response):
        new_user_data = self.chats.add_participant(**request.media)
        response.media = {
            'message': f'user {new_user_data.user_id} was added to chat {new_user_data.chat_id}'
            }
        response.status = falcon.HTTP_201

    @join_point
    def on_post_remove_participant(self, request: Request, response: Response):
        removed_user_data = self.chats.remove_participant(**request.media)
        response.media = {
            'message': f'user {removed_user_data.user_id} was removed from chat {removed_user_data.chat_id}'
            }
        response.status = falcon.HTTP_200  # FIXME With 204 status there is no return

    @join_point
    def on_post_delete_chat(self, request: Request, response: Response):
        self.chats.delete_chat(**request.media)
        response.status = falcon.HTTP_204

    def on_post_quit_chat(self, request: Request, response: Response):
        quit_data = self.chats.quit_chat(**request.media)
        response.media = {
            'message': f'user {quit_data.user_id} quited from chat {quit_data.chat_id}'
            }
        response.status = falcon.HTTP_200


@component
class Users:
    users: services.Users

    @join_point
    def on_post_register(self, request: Request, response: Response):
        user_info = self.users.register_user(**request.media)
        response.media = {
            "message": "Account successfully created",
            "user_info": user_info.dict()
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