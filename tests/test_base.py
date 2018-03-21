import unittest
from bigcommerce.resources import Mapping, Orders, ApiResource, OrderShipments, Products, CountryStates,\
                                  OrderCoupons, Webhooks, GoogleProductSearchMappings
from mock import MagicMock


class TestMapping(unittest.TestCase):
    def test_init(self):
        result = {
            'coupons': {'url': 'blah'},
            'id': 1
        }

        map = Orders(result)
        self.assertEqual(map.id, 1)
        self.assertEqual(map['id'], 1)

        self.assertNotIsInstance(map.coupons, dict)

    def test_str(self):
        map = Mapping({'id': 1, '_connection': MagicMock()})
        self.assertEqual(str(map), str({'id': 1}))


class TestApiResource(unittest.TestCase):
    def test_create_object(self):
        # Test with a single object
        result = {'id': 1}
        object = ApiResource._create_object(result, MagicMock())
        self.assertEqual(object.id, 1)

        # Test with a list
        results = [{'id': 1}, {'id': 2}, {'id': 3}]
        objects = ApiResource._create_object(results, MagicMock)
        self.assertIsInstance(objects, list)
        for object in objects:
            self.assertIsNotNone(object.id)
            self.assertIsNotNone(object._connection)

    def test_get(self):
        connection = MagicMock()
        connection.make_request.return_value = {'id': 1}

        result = Orders.get(1, connection)
        self.assertIsInstance(result, Orders)
        self.assertEqual(result.id, 1)

        connection.make_request.assert_called_once_with('GET', 'orders/1', None, {}, None)


class TestApiSubResource(unittest.TestCase):
    def test_get(self):
        connection = MagicMock()
        connection.make_request.return_value = {'id': 2}

        result = OrderCoupons.get(1, 2, connection)
        self.assertIsInstance(result, OrderCoupons)
        self.assertEqual(result.id, 2)

        connection.make_request.assert_called_once_with('GET', 'orders/1/coupons/2', None, {}, None)

    def test_parent_id(self):
        coupon = OrderCoupons({'id': 2, 'order_id': 1})
        self.assertEqual(coupon.parent_id(), 1)


class TestCreateableApiResource(unittest.TestCase):
    def test_create(self):
        connection = MagicMock()
        connection.make_request.return_value = {'id': 1}

        result = Orders.create(connection, name="Hello")
        self.assertIsInstance(result, Orders)
        self.assertEqual(result.id, 1)
        connection.make_request.assert_called_once_with('POST', 'orders', {'name': 'Hello'}, None, None)


class TestCreateableApiSubResource(unittest.TestCase):
    def test_create(self):
        connection = MagicMock()
        connection.make_request.return_value = {'id': 2}

        result = OrderShipments.create(1, connection, name="Hello")
        self.assertIsInstance(result, OrderShipments)
        self.assertEqual(result.id, 2)
        connection.make_request.assert_called_once_with('POST', 'orders/1/shipments', {'name': 'Hello'}, None, None)


class TestListableApiResource(unittest.TestCase):
    def test_all(self):
        connection = MagicMock()
        connection.make_request.return_value = [{'id': 1}, {'id': 2}, {'id': 2}]

        result = Orders.all(connection, limit=3)
        self.assertEqual(len(list(result)), 3)
        connection.make_request.assert_called_once_with('GET', 'orders', None, {'limit': 3}, None)


class TestListableApiSubResource(unittest.TestCase):
    def test_all(self):
        connection = MagicMock()
        connection.make_request.return_value = [{'id': 1}, {'id': 2}]

        result = OrderCoupons.all(1, connection, limit=2)
        self.assertEqual(len(result), 2)
        connection.make_request.assert_called_once_with('GET', 'orders/1/coupons', None, {'limit': 2}, None)

    def test_google_mappings(self):
        connection = MagicMock()
        connection.make_request.return_value = [{'id': 1}, {'id': 2}]

        result = GoogleProductSearchMappings.all(1, connection, limit=2)
        self.assertEqual(len(result), 2)
        connection.make_request.assert_called_once_with('GET', 'products/1/googleproductsearch', None, {'limit': 2}, None)


class TestUpdateableApiResource(unittest.TestCase):
    def test_update(self):
        connection = MagicMock()
        connection.make_request.return_value = {'id': 1}

        order = Orders({'id': 1}, _connection=connection)
        new_order = order.update(name='order')
        self.assertIsInstance(new_order, Orders)

        connection.make_request.assert_called_once_with('PUT', 'orders/1', {'name': 'order'}, None, None)


class TestUpdateableApiSubResource(unittest.TestCase):
    def test_update(self):
        connection = MagicMock()
        connection.make_request.return_value = {'id': 1}

        order = OrderShipments({'id': 1, 'order_id': 2}, _connection=connection)
        new_order = order.update(tracking_number='1234')
        self.assertIsInstance(new_order, OrderShipments)

        connection.make_request.assert_called_once_with('PUT', 'orders/2/shipments/1', {'tracking_number': '1234'},
                                                        None, None)


class TestDeleteableApiResource(unittest.TestCase):
    def test_delete_all(self):
        connection = MagicMock()
        connection.make_request.return_value = {}

        self.assertEqual(Orders.delete_all(connection), {})

        connection.make_request.assert_called_once_with('DELETE', 'orders', None, None, None)

    def test_delete(self):
        connection = MagicMock()
        connection.make_request.return_value = {}

        order = Orders({'id': 1}, _connection=connection)

        self.assertEqual(order.delete(), {})

        connection.make_request.assert_called_once_with('DELETE', 'orders/1', None, None, None)


class TestDeleteableApiSubResource(unittest.TestCase):
    def test_delete_all(self):
        connection = MagicMock()
        connection.make_request.return_value = {}

        self.assertEqual(OrderShipments.delete_all(1, connection=connection), {})

        connection.make_request.assert_called_once_with('DELETE', 'orders/1/shipments', None, None, None)

    def test_delete(self):
        connection = MagicMock()
        connection.make_request.return_value = {}

        shipment = OrderShipments({'id': 1, 'order_id': 2, '_connection': connection})
        self.assertEqual(shipment.delete(), {})

        connection.make_request.assert_called_once_with('DELETE', 'orders/2/shipments/1', None, None, None)


class TestCountableApiResource(unittest.TestCase):
    def test_count(self):
        connection = MagicMock()
        connection.make_request.return_value = {'count': 2}

        self.assertEqual(Products.count(connection, is_visible=True), 2)
        connection.make_request.assert_called_once_with('GET', 'products/count', None, {'is_visible': True}, None)


class TestCountableApiSubResource(unittest.TestCase):
    def test_count(self):
        connection = MagicMock()
        connection.make_request.return_value = {'count': 2}

        self.assertEqual(CountryStates.count(1, connection=connection, is_visible=True), 2)
        connection.make_request.assert_called_once_with('GET', 'countries/1/states/count',
                                                        None, {'is_visible': True}, None)

    def test_count_with_custom_count_path(self):
        connection = MagicMock()
        connection.make_request.return_value = {'count': 2}

        self.assertEqual(OrderShipments.count(connection=connection, is_visible=True), 2)
        connection.make_request.assert_called_once_with('GET', 'orders/shipments/count',
                                                        None, {'is_visible': True}, None)
