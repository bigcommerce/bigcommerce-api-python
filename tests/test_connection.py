import json
import unittest
from bigcommerce.connection import Connection, OAuthConnection
from bigcommerce.exception import ServerException, ClientRequestException, RedirectionException
from mock import patch, MagicMock


class TestConnection(unittest.TestCase):
    def test_create(self):
        connection = Connection(host='store.mybigcommerce.com', auth=('user', 'abcdef'))
        self.assertTupleEqual(connection._session.auth, ('user', 'abcdef'))

    def test_full_path(self):
        connection = Connection(host='store.mybigcommerce.com', auth=('user', 'abcdef'))
        self.assertEqual(connection.full_path('time'), 'https://store.mybigcommerce.com/api/v2/time')

    def test_run_method(self):
        connection = Connection(host='store.mybigcommerce.com', auth=('user', 'abcdef'))
        connection._session.request = MagicMock()

        # Call with nothing
        connection._run_method('GET', '')
        connection._session.request.assert_called_once_with('GET', 'https://store.mybigcommerce.com/api/v2/',
                                                            data=None, timeout=7.0, headers={})
        connection._session.request.reset_mock()

        # A simple request
        connection._run_method('GET', 'time')
        connection._session.request.assert_called_once_with('GET', 'https://store.mybigcommerce.com/api/v2/time',
                                                            data=None, timeout=7.0, headers={})
        connection._session.request.reset_mock()

        # A request with data
        data = {
            'name': 'Shirt',
            'price': 25.00
        }

        connection._run_method('POST', '/products', data)

        connection._session.request.assert_called_once_with('POST', 'https://store.mybigcommerce.com/api/v2/products',
                                                            data=json.dumps(data), timeout=7.0,
                                                            headers={'Content-Type': 'application/json'})
        connection._session.request.reset_mock()

        # A request with filters
        connection._run_method('GET', '/orders', query={'limit': 50})
        connection._session.request.assert_called_once_with('GET',
                                                            'https://store.mybigcommerce.com/api/v2/orders?limit=50',
                                                            data=None, timeout=7.0, headers={})
        connection._session.request.reset_mock()

    def test_handle_response(self):
        connection = Connection('store.mybigcommerce.com', ('user', 'abcdef'))
        # A normal, 200-ok response
        data = {
            'name': 'Shirt'
        }
        res = MagicMock()
        res.headers = {'Content-Type': 'application/json'}
        res.status_code = 200
        res.content = json.dumps(data)
        res.json.return_value = data
        self.assertEqual(connection._handle_response('products/1', res), data)

        res.status_code = 500
        self.assertRaisesHttpException(ServerException,
                                       lambda: connection._handle_response('products/1', res),
                                       # Test all of the properties of a HttpException
                                       500,
                                       {'Content-Type': 'application/json'},
                                       json.dumps(data))

        res.status_code = 404
        self.assertRaisesHttpException(ClientRequestException,
                                       lambda: connection._handle_response('products/1', res), 404)

        res.status_code = 301
        self.assertRaisesHttpException(RedirectionException,
                                       lambda: connection._handle_response('products/1', res), 301)

    def assertRaisesHttpException(self, exec_class, callable, status_code=None, headers=None, content=None):
        try:
            callable()
            self.assertFail()
        except exec_class as e:
            if status_code:
                self.assertEqual(status_code, e.status_code)
            if headers:
                self.assertDictEqual(headers, e.headers)
            if content:
                self.assertEqual(content, e.content)


class TestOAuthConnection(unittest.TestCase):
    def test_full_path(self):
        connection = OAuthConnection(client_id='123', store_hash='abcdef')
        self.assertEqual(connection.full_path('time'), 'https://api.bigcommerce.com/stores/abcdef/v2/time')

    def test_alternate_api_endpoint(self):
        connection = OAuthConnection(client_id='123', store_hash='abcdef', host='barbaz.com')
        self.assertEqual(connection.full_path('time'), 'https://barbaz.com/stores/abcdef/v2/time')

    def test_verify_payload(self):
        """Decode and verify signed payload."""
        payload = "eyJ1c2VyIjp7ImlkIjo3MiwiZW1haWwiOiJqYWNraWUuaHV5bmh" \
                  "AYmlnY29tbWVyY2UuY29tIn0sInN0b3JlX2hhc2giOiJsY3R2aD" \
                  "V3bSIsInRpbWVzdGFtcCI6MTM4OTA1MDMyNy42NTc5NjI2fQ==." \
                  "ZTViYzAzNTM2MGFjM2M2YTVkZjFmNzFlYTk4NTY1ODZiMzkxODZmZDExZTdjZGFmOGEzN2E3YTEzNGQ0MmExYw=="
        client_secret = 'ntb1kcxa1do55wf0h25ps7h94fnsoi6'
        user_data = OAuthConnection.verify_payload(payload, client_secret)
        self.assertTrue(user_data) # otherwise verification has failed
        self.assertEqual(user_data['user']['id'], 72)
        self.assertEqual(user_data['user']['email'], "jackie.huynh@bigcommerce.com")

        # Try again with a fake payload
        payload = "notevenreal7ImlkIjo3MiwiZW1haWwiOiJqYWNraWUuaHV5bmh" \
                  "AYmlnY29tbWVyY2UuY29tIn0sInN0b3JlX2hhc2giOiJsY3R2aD" \
                  "V3bSIsInRpbWVzdGFtcCI6MTM4OTA1MDMyNy42NTc5NjI2fQ==." \
                  "quitefakeTM2MGFjM2M2YTVkZjFmNzFlYTk4NTY1ODZiMzkxODZmZDExZTdjZGFmOGEzN2E3YTEzNGQ0MmExYw=="

        user_data = OAuthConnection.verify_payload(payload, client_secret)
        self.assertFalse(user_data)

    def test_fetch_token(self):
        client_id = 'abc123'
        client_secret = '123abc'
        code = 'hellosecret'
        context = 'stores/abc'
        scope = 'store_v2_products'
        redirect_uri = 'http://localhost/callback'
        result = {'access_token': '12345abcdef'}

        connection = OAuthConnection(client_id, store_hash='abc')
        connection.post = MagicMock()
        connection.post.return_value = result

        res = connection.fetch_token(client_secret, code, context, scope, redirect_uri)
        self.assertEqual(res, result)
        self.assertDictEqual(connection._session.headers,
                             {'X-Auth-Client': 'abc123', 'X-Auth-Token': '12345abcdef',
                              'Accept': 'application/json', 'Accept-Encoding': 'gzip'})
        connection.post.assert_called_once_with('https://login.bigcommerce.com/oauth2/token',
                                                {
                                                    'client_id': client_id,
                                                    'client_secret': client_secret,
                                                    'code': code,
                                                    'context': context,
                                                    'scope': scope,
                                                    'grant_type': 'authorization_code',
                                                    'redirect_uri': redirect_uri
                                                },
                                                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
