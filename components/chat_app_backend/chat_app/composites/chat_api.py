from sqlalchemy import create_engine
from classic.sql_storage import TransactionContext
from chat_app.application import services
from chat_app.adapters import chat_api, database

class Settings:
    db = database.Settings()
    chat_api = chat_api.Settings()

class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)
    context = TransactionContext(bind=engine)
    users_repo = database.repositories.UsersRepo(context=context)
    chats_repo = database.repositories.ChatsRepo(context=context)
    messages_repo = database.repositories.MessagesRepo(context=context)
    statuses_repo = database.repositories.StatusesRepo(context=context)

class Application:
    chats = services.Chats(
        chats_repo=DB.chats_repo,
        users_repo=DB.users_repo
        )

    users = services.Users(
        users_repo=DB.users_repo
        )

    is_dev_mode = Settings.chat_api.IS_DEV_MODE
    allow_origins = Settings.chat_api.ALLOW_ORIGINS


app = chat_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    allow_origins=Application.allow_origins,
    chats=Application.chats,
    users=Application.users
    )

class Aspects:
    services.join_points.join(DB.context)
    chat_api.join_points.join(DB.context)

if __name__ == '__main__':
    from wsgiref import simple_server
    with simple_server.make_server(
            host='localhost', port=8123, app=app) as httpd:
        httpd.serve_forever(0.5)