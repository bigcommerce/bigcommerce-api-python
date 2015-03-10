import os
import unittest

import bigcommerce.api
from bigcommerce.connection import Connection, OAuthConnection
from bigcommerce.resources import ApiResource
from mock import MagicMock, patch, Mock

class TestBigcommerceApi(unittest.TestCase):
    """ Test API client creation and helpers"""

    def test_create_basic(self):
        api = bigcommerce.api.BigcommerceApi(host='store.mybigcommerce.com', basic_auth=('admin', 'abcdef'))
        self.assertIsInstance(api.connection, Connection)
        self.assertNotIsInstance(api.connection, OAuthConnection)

    def test_create_oauth(self):
        api = bigcommerce.api.BigcommerceApi(client_id='123456', store_hash='abcdef', access_token='123abc')
        self.assertIsInstance(api.connection, OAuthConnection)

    def test_default_api_endpoint(self):
        api = bigcommerce.api.BigcommerceApi(client_id='123456', store_hash='abcdef', access_token='123abc')
        self.assertEqual(api.api_service, 'api.bigcommerce.com')

    def test_alternate_api_endpoint_from_env(self):
        os.environ['BC_API_ENDPOINT'] = 'foobar.com'
        api = bigcommerce.api.BigcommerceApi(client_id='123456', store_hash='abcdef', access_token='123abc')
        self.assertEqual(api.api_service, 'foobar.com')
        del os.environ['BC_API_ENDPOINT']

    def test_default_auth_endpoint(self):
        api = bigcommerce.api.BigcommerceApi(client_id='123456', store_hash='abcdef', access_token='123abc')
        self.assertEqual(api.auth_service, 'login.bigcommerce.com')

    def test_alternate_auth_endpoint_from_env(self):
        os.environ['BC_AUTH_SERVICE'] = 'foobar.com'
        api = bigcommerce.api.BigcommerceApi(client_id='123456', store_hash='abcdef', access_token='123abc')
        self.assertEqual(api.auth_service, 'foobar.com')
        del os.environ['BC_AUTH_SERVICE']

    def test_create_incorrect_args(self):
        self.assertRaises(Exception, lambda: bigcommerce.api.BigcommerceApi(client_id='123', basic_auth=('admin', 'token')))


class TestApiResourceWrapper(unittest.TestCase):

    def test_create(self):
        api = MagicMock()
        api.connection = MagicMock()

        wrapper = bigcommerce.api.ApiResourceWrapper('ApiResource', api)
        self.assertEqual(api.connection, wrapper.connection)
        self.assertEqual(wrapper.resource_class, ApiResource)

        wrapper = bigcommerce.api.ApiResourceWrapper(ApiResource, api)
        self.assertEqual(wrapper.resource_class, ApiResource)

    def test_str_to_class(self):
        cls = bigcommerce.api.ApiResourceWrapper.str_to_class('ApiResource')
        self.assertEqual(cls, ApiResource)

        self.assertRaises(AttributeError, lambda: bigcommerce.api.ApiResourceWrapper.str_to_class('ApiResourceWhichDoesNotExist'))

    @patch.object(ApiResource, 'get')
    def test_get_attr(self, patcher):
        api = MagicMock()
        api.connection = MagicMock()

        result = {'id': 1}
        patcher.return_value = result

        wrapper = bigcommerce.api.ApiResourceWrapper('ApiResource', api)
        self.assertEqual(wrapper.get(1), result)
        patcher.assert_called_once_with(1, connection=api.connection)



