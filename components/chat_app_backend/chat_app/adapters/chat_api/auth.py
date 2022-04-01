import os

import falcon
import jwt
from classic.components import component
from classic.http_auth import Group, Permission, strategies, errors
from classic.http_auth import Authenticator
from classic.http_auth.interfaces import AuthStrategy
from classic.http_auth.entities import Client
from classic.http_auth.strategies import JWT


class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    ADMINS = Group('admins', permissions=(Permissions.FULL_CONTROL,))


ALL_GROUPS = (Groups.ADMINS,)


class HeaderIDStrategy(AuthStrategy):
    def get_client(self, request: 'falcon.Request', **static_client_params) -> Client:
        token = request.get_header('user_id')
        if not token:
            raise errors.AuthenticationError('Token decoding error')

        client = Client(
            user_id=request.get_header('user_id'),
            login='',
            name=''
            )
        return client


class JWTIDStrategy(JWT):
    def __init__(self, *args, **kwargs):
        super(JWTIDStrategy, self).__init__(*args, **kwargs)

    @staticmethod
    def create_token(user_id: int, username: str):
        token = jwt.encode(
            payload=dict(sub=user_id, login=username, name=username),
            key=os.getenv('JWT_SECRET'),
            algorithm='HS256'
            )
        return token


header_id_strategy = HeaderIDStrategy()
jwt_id_strategy = JWTIDStrategy(secret_key=os.getenv('JWT_SECRET'))

test_strategy = strategies.Dummy(
    user_id=1,
    login='test_login',
    name='test_name',
    groups=(Groups.ADMINS.name,),
    )


class SimpleAuthenticator(Authenticator):
    def __init__(self, *args, **kwargs):
        super(SimpleAuthenticator, self).__init__(*args, **kwargs)

    def create_token(self, user_id: int, username: str):
        for strategy in self.strategies:
            if hasattr(strategy, 'create_token'):
                token = strategy.create_token(user_id, username)
                return token
        return None

