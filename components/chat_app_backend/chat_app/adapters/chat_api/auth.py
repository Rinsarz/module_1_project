import falcon
from classic.components import component
from classic.http_auth import Group, Permission, strategies, errors
from classic.http_auth import Authenticator
from classic.http_auth.interfaces import AuthStrategy
from classic.http_auth.entities import Client


class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    ADMINS = Group('admins', permissions=(Permissions.FULL_CONTROL,))


ALL_GROUPS = (Groups.ADMINS,)


class HeaderID(AuthStrategy):
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


header_id_strategy = HeaderID()

test_strategy = strategies.Dummy(
    user_id=1,
    login='test_login',
    name='test_name',
    groups=(Groups.ADMINS.name,),
    )


@component
class SimpleAuthenticator(Authenticator):
    def get_client(self, request):
        pass

    def auth(self, request: falcon.Request, resource_name: str = ""):
        client = self.get_client(request)