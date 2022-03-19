import falcon
from classic.components import component
from classic.http_auth import authenticator_needed, authenticate
from falcon import Request, Response

from chat_app.application import services
from .join_points import join_point


@authenticator_needed
@component
class Chats:
    chats: services.Chats

    @authenticate
    @join_point
    def on_get_show_messages(self, request: Request, response: Response):
        messages = self.chats.get_messages(
            user_id=request.context.client.user_id,
            **request.params)
        if len(messages) > 0:
            response.media = {
                'messages': [{
                    'message_id': message.message_id,
                    'message_text': message.message_text,
                    'message_author_id': message.user_id,
                    'message_created': message.created.strftime("%d-%m-%Y %H:%M:%S")
                    }
                    for message in messages]
                }
            response.status = falcon.HTTP_200
        else:
            response.media = {
                'message': 'No messages in this chat yet'
                }
            response.status = falcon.HTTP_404

    @authenticate
    @join_point
    def on_post_add_chat(self, request: Request, response: Response):
        self.chats.create_chat(
            creator_id=request.context.client.user_id,
            **request.media)
        response.media = {
            'message': 'chat was successfully created'
            }
        response.status = falcon.HTTP_201

    @authenticate
    @join_point
    def on_post_update_chat(self, request: Request, response: Response):
        self.chats.update_chat_info(
            user_id=request.context.client.user_id,
            **request.media
            )
        response.media = {
            'message': 'chat was successfully updated'
            }
        response.status = falcon.HTTP_200


    @authenticate
    @join_point
    def on_post_send_message(self, request: Request, response: Response):
        self.chats.send_message(
            user_id=request.context.client.user_id,
            **request.media)
        response.media = {
            'message': 'message was sent'
            }
        response.status = falcon.HTTP_200

    @authenticate
    @join_point
    def on_get_chat_info(self, request: Request, response: Response):
        chat = self.chats.get_chat_info(
            user_id=request.context.client.user_id,
            **request.params)
        response.media = {
            'chat id': chat.chat_id,
            'chat info': chat.info,
            'chat creator id': chat.creator_id,
            # 'chat users:': [{user.user_id: user.username} for user in chat.users]
            }
        response.status = falcon.HTTP_200

    @authenticate
    @join_point
    def on_get_chat_participants(self, request: Request, response: Response):
        users_short = self.chats.get_chat_participants(
            user_id=request.context.client.user_id,
            **request.params)
        response.media = {
            'chat participants': [
                {
                    'id': user.user_id,
                    'username': user.username
                    } for user in users_short]
            }
        response.status = falcon.HTTP_200

    @authenticate
    @join_point
    def on_post_add_participant(self, request: Request, response: Response):
        new_user_data = self.chats.add_participant(
            user_id=request.context.client.user_id,
            **request.media)
        response.media = {
            'message': f'user {new_user_data.user_id} was added to chat {new_user_data.chat_id}'
            }
        response.status = falcon.HTTP_201

    @authenticate
    @join_point
    def on_post_remove_participant(self, request: Request, response: Response):
        removed_user_data = self.chats.remove_participant(
            user_id=request.context.client.user_id,
            **request.media)
        response.media = {
            'message': f'user {removed_user_data.user_id} was removed from chat {removed_user_data.chat_id}'
            }
        response.status = falcon.HTTP_200  # FIXME With 204 status there is no return

    @authenticate
    @join_point
    def on_post_delete_chat(self, request: Request, response: Response):
        self.chats.delete_chat(
            user_id=request.context.client.user_id,
            **request.media)
        response.status = falcon.HTTP_204

    @authenticate
    def on_post_quit_chat(self, request: Request, response: Response):
        quit_data = self.chats.quit_chat(
            user_id=request.context.client.user_id,
            **request.media)
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
    def on_post_login(self, request: Request, response: Response):
        pass

    # @join_point
    # def on_get_user_info(self, request: Request, response: Response):
    #     user = self.users.get_user_by_id(**request.media)
    #     response.media = {
    #         "id": user.user_id,
    #         "username": user.username,
    #         "email": user.email
    #         }