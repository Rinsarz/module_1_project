from sqlalchemy.orm import registry, relationship
from chat_app.application import dataclasses
from . import tables

mapper = registry()
mapper.map_imperatively(
    dataclasses.Chat,
    tables.chats,
    properties={
        'users': relationship(
            dataclasses.User,
            secondary=tables.chat_user,
            ),
        'messages': relationship(
            dataclasses.Message,
            lazy='subquery',
            cascade='all, delete-orphan'
            ),
        'creator': relationship(
            dataclasses.User,
            lazy='joined',
            uselist=False
            )
        })

mapper.map_imperatively(
    dataclasses.User,
    tables.users,
    properties={
        'chats': relationship(
            dataclasses.Chat,
            secondary=tables.chat_user
            )
        }
    )

mapper.map_imperatively(
    dataclasses.Message,
    tables.messages,
    properties={
        'user': relationship(
            dataclasses.User,
            lazy='joined',
            uselist=False
            )
        })

mapper.map_imperatively(
    dataclasses.ChatUser,
    tables.chat_user,
    properties={
        'status': relationship(
            dataclasses.Chat,
            lazy='joined',
            uselist=False,
            )
        }
    )

mapper.map_imperatively(
    dataclasses.Status,
    tables.statuses
    )
