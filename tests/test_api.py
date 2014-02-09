import unittest

import bigcommerce.api
from bigcommerce.connection import Connection, OAuthConnection
from bigcommerce.resources import ApiResource
from mock import MagicMock, patch, Mock

__author__ = 'tim'


class TestBigcommerceApi(unittest.TestCase):
    """ Test API client creation and helpers"""

    def test_create_basic(self):
        with patch('requests.Session') as mock:
            instance = mock.return_value
            mock_result = Mock()
            mock_result.status_code = 200
            mock_result.json.return_value = {}
            instance.request.return_value = mock_result
            api = bigcommerce.api.BigcommerceApi(store_endpoint='https://store.mybigcommerce.com', basic_auth=('admin', 'abcdef'))
            self.assertIsInstance(api.connection, Connection)
            self.assertNotIsInstance(api.connection, OAuthConnection)

    def test_create_oauth(self):
        with patch('requests.Session') as mock:
            instance = mock.return_value
            mock_result = Mock()
            mock_result.status_code = 200
            mock_result.json.return_value = {}
            instance.request.return_value = mock_result
            api = bigcommerce.api.BigcommerceApi(client_id='123456', store_hash='abcdef', access_token='123abc')
            self.assertIsInstance(api.connection, OAuthConnection)

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

    def test_get_attr(self):
        api = MagicMock()
        api.connection = MagicMock()

        ApiResource.get = MagicMock()
        mock_return = Mock()
        ApiResource.get.return_value = mock_return

        wrapper = bigcommerce.api.ApiResourceWrapper('ApiResource', api)
        self.assertEqual(wrapper.get(1), mock_return)
        ApiResource.get.assert_called_once_with(1, connection=api.connection)



