from sqlalchemy.orm import registry, relationship
from chat_app.application import dataclasses
from . import tables

mapper = registry()
mapper.map_imperatively(
    dataclasses.Chat,
    tables.chats,
    properties={
        'users': relationship(
            dataclasses.ChatUser,
            cascade='all, delete-orphan'
            ),
        'messages': relationship(
            dataclasses.Message,
            cascade='all, delete-orphan'
            )
        }
    )

mapper.map_imperatively(
    dataclasses.User,
    tables.users,
    )

mapper.map_imperatively(
    dataclasses.Message,
    tables.messages,
    )

mapper.map_imperatively(
    dataclasses.ChatUser,
    tables.chat_user,
    )