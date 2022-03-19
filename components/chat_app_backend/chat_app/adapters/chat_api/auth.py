import falcon
from classic.components import component
from classic.http_auth import Group, Permission
from classic.http_auth import Authenticator


class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    ADMINS = Group('admins', permissions=(Permissions.FULL_CONTROL,))


ALL_GROUPS = (Groups.ADMINS,)


@component
class SimpleAuthenticator(Authenticator):
    def get_client(self, request):
        pass

    def auth(self, request: falcon.Request, resource_name: str = ""):
        client = self.get_client(request)