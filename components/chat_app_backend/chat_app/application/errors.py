from classic.app.errors import AppError


class NoChat(AppError):
    msg_template = "No chat with id {chat_id}"
    code = 'chat.no_chat'

class NoUser(AppError):
    msg_template = "No user with id {user_id}"
    code = 'chat.no_user'

class NoPermission(AppError):
    msg_template = "User with id {user_id} has no permissions to do this"
    code = 'chat.no_permission'