import os
import sys
from bigcommerce import connection
from bigcommerce.resources import *  # Needed for ApiResourceWrapper dynamic loading


class BigcommerceApi(object):
    def __init__(self, host=None, basic_auth=None,
                 client_id=None, store_hash=None, access_token=None, rate_limiting_management=None):
        self.api_service = os.getenv('BC_API_ENDPOINT', 'api.bigcommerce.com')
        self.auth_service = os.getenv('BC_AUTH_SERVICE', 'login.bigcommerce.com')

        if host and basic_auth:
            self.connection = connection.Connection(host, basic_auth)
        elif client_id and store_hash:
            self.connection = connection.OAuthConnection(client_id, store_hash, access_token, self.api_service,
                                                         rate_limiting_management=rate_limiting_management)
        else:
            raise Exception("Must provide either (client_id and store_hash) or (host and basic_auth)")

    def oauth_fetch_token(self, client_secret, code, context, scope, redirect_uri):
        if isinstance(self.connection, connection.OAuthConnection):
            token_url = 'https://%s/oauth2/token' % self.auth_service
            return self.connection.fetch_token(client_secret, code, context, scope, redirect_uri, token_url)

    @classmethod
    def oauth_verify_payload(cls, signed_payload, client_secret):
        return connection.OAuthConnection.verify_payload(signed_payload, client_secret)

    def __getattr__(self, item):
        return ApiResourceWrapper(item, self)


class ApiResourceWrapper(object):
    """
    Provides dot access to each of the API resources
    while proxying the connection parameter so that
    the user does not need to know it exists
    """
    def __init__(self, resource_class, api):
        """
        :param resource_class: String or Class to proxy
        :param api: API whose connection we want to use
        :return: A wrapper instance
        """
        if isinstance(resource_class, str):
            self.resource_class = self.str_to_class(resource_class)
        else:
            self.resource_class = resource_class
        self.connection = api.connection

    def __getattr__(self, item):
        """
        Proxies access to all methods on the resource class,
        injecting the connection parameter before any
        other arguments

        TODO: Distinguish between methods and attributes
        on the resource class?
        """
        return lambda *args, **kwargs: (getattr(self.resource_class, item))(*args, connection=self.connection, **kwargs)

    @classmethod
    def str_to_class(cls, str):
        """
        Transforms a string class name into a class object
        Assumes that the class is already loaded.
        """
        return getattr(sys.modules[__name__], str)
