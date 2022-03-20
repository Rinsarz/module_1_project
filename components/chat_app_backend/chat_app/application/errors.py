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


class NoParticipant(AppError):
    msg_template = "There is no user with id {user_id} in the chat"
    code = 'chat.no_participant'


class AlreadyParticipant(AppError):
    msg_template = "User with id {user_id} is already in the chat"
    code = 'chat.already_participant'


class NotRegistered(AppError):
    msg_template = "User is not registered or data is not correct"
    code = 'chat.not_registered'


class AlreadyRegistered(AppError):
    msg_template = "User with email {email} is already registered"
    code = 'chat.already_registered'