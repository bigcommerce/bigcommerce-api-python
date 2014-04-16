from .base import *


class Orders(ListableApiResource, CreateableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'orders'

    def coupons(self, id=None):
        if id:
            return OrderCoupons.get(self.id, id, connection=self._connection)
        else:
            return OrderCoupons.all(self.id, connection=self._connection)

    def products(self, id=None):
        if id:
            return OrderProducts.get(self.id, id, connection=self._connection)
        else:
            return OrderProducts.all(self.id, connection=self._connection)

    def shipments(self, id=None):
        if id:
            return OrderShipments.get(self.id, id, connection=self._connection)
        else:
            return OrderShipments.all(self.id, connection=self._connection)

    def shipping_addresses(self, id=None):
        if id:
            return OrderShippingAddresses.get(self.id, id, connection=self._connection)
        else:
            return OrderShippingAddresses.all(self.id, connection=self._connection)


class OrderCoupons(ListableApiSubResource):
    resource_name = 'coupons'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderProducts(ListableApiSubResource):
    resource_name = 'products'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderShipments(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'shipments'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderShippingAddresses(ListableApiSubResource):
    resource_name = 'shipping_addresses'
    parent_resource = 'orders'
    parent_key = 'order_id'
