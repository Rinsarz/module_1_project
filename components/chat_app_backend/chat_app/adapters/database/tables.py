from sqlalchemy import Table, \
    MetaData, Column, Integer, String, \
    ForeignKey, DateTime

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

# даем имя схемы только для БД MSSQL, связано с инфраструктурными особенностями
# metadata = MetaData(naming_convention=naming_convention, schema='app')

# metadata = MetaData(naming_convention=naming_convention)
metadata = MetaData()
users = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False),
    Column('email', String, nullable=False),
    )

statuses = Table(
    'statuses',
    metadata,
    Column('status_id', Integer, primary_key=True, autoincrement=True),
    Column('status_name', String, nullable=False),
    )

chat_user = Table(
    'chat_user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', ForeignKey('chats.chat_id'), nullable=False),
    Column('user_id', ForeignKey('users.user_id'), nullable=False),
    Column('status_id', String, nullable=True),
    Column('changed', String, nullable=True),
    )

chats = Table(
    'chats',
    metadata,
    Column('chat_id', Integer, primary_key=True, autoincrement=True),
    Column('creator_id', ForeignKey('users.user_id'), nullable=False),
    Column('info', String, nullable=False),
    )

messages = Table(
    'messages',
    metadata,
    Column('message_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id'), nullable=False),
    Column('chat_id', ForeignKey('chats.chat_id'), nullable=False),
    Column('message_text', String, nullable=False),
    Column('created', String, nullable=False),
    )