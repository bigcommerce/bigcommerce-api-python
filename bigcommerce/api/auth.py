import connection
import logging

log = logging.getLogger("bigcommerce.api.auth")


def basic_login(host, username, apikey):
    log.debug("Login to %s as %s".format(host, username))
    connection.client = connection.Connection(host, (username, apikey))


def oauth_configure(client_id, store_hash, access_token=None):
    connection.client = connection.OAuthConnection(client_id, store_hash, access_token)


def oauth_fetch_token(client_secret, code, context, scope, redirect_uri):
    if connection.client and isinstance(connection.client, connection.OAuthConnection):
        return connection.client.fetch_token(client_secret, code, context, scope, redirect_uri)


def oauth_verify_payload(signed_payload, client_secret):
    return connection.OAuthConnection.verify_payload(signed_payload, client_secret)