"""
Connection Module

Handles put and get operations to the Bigcommerce REST API
"""
import base64
import hashlib
import hmac
import json

import streql
import requests

from bigcommerce import Connection


class OAuthConnection(Connection):
    """
    Class for making OAuth requests on the Bigcommerce v2 API as an integrated app.

    Providing a value for access_token allows immediate access to resources within registered scope.
    Otherwise, you may use fetch_token with the code, context, and scope passed to your application's callback url
    to retrieve an access token.

    The verify_payload method is also provided for authenticating signed payloads passed to an application's load url.
    """

    def __init__(self, client_id, store_hash, access_token=None,
                 host='api.bigcommerceapp.com', api_path='/stores/{}/v2/{}', map_wrap=True):
        self.client_id = client_id
        self.store_hash = store_hash

        self.host = host
        self.api_path = api_path

        self.timeout = 7.0  # can attach to session?
        self._map_wrap = map_wrap

        self._session = requests.Session()
        self._session.headers = {"Accept": "application/json"}
        if access_token and store_hash:
            self._session.headers.update(self._oauth_headers(client_id, access_token))

        # TODO find meta info new path (/store gives a "your scope does not include this resource")
        self.__resource_meta = {}  # self.get()  # retrieve metadata about urls and resources
        self._last_response = None  # for debugging

    def full_path(self, url):
        return "https://" + self.host + self.api_path.format(self.store_hash, url)

    @staticmethod
    def _oauth_headers(cid, atoken):
        return {'X-Auth-Client': cid,
                'X-Auth-Token': atoken}

    @staticmethod
    def verify_payload(signed_payload, client_secret):
        """
        Given a signed payload (usually passed as parameter in a GET request to the app's load URL) and a client secret,
        authenticates the payload and returns the user's data, or False on fail.

        Uses constant-time str comparison to prevent vulnerability to timing attacks.
        """
        encoded_json, encoded_hmac = signed_payload.split('.')
        dc_json = base64.b64decode(encoded_json)
        signature = base64.b64decode(encoded_hmac)
        expected_sig = hmac.new(client_secret, base64.b64decode(encoded_json), hashlib.sha256).hexdigest()
        authorised = streql.equals(signature, expected_sig)
        return json.loads(dc_json) if authorised else False

    def fetch_token(self, client_secret, code, context, scope, redirect_uri,
                    token_url='https://login.bigcommerceapp.com/oauth2/token'):
        """
        Fetches a token from given token_url, using given parameters, and sets up session headers for
        future requests.
        redirect_uri should be the same as your callback URL.
        code, context, and scope should be passed as parameters to your callback URL on app installation.

        Raises HttpException on failure (same as Connection methods).
        """
        res = self.post(token_url, {'client_id': self.client_id,
                                    'client_secret': client_secret,
                                    'code': code,
                                    'context': context,
                                    'scope': scope,
                                    'grant_type': 'authorization_code',
                                    'redirect_uri': redirect_uri},
                        headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self._session.headers.update(self._oauth_headers(self.client_id, res['access_token']))
        return res