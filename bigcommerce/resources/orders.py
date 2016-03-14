from .base import *


class Orders(ListableApiResource, CreateableApiResource,
             UpdateableApiResource, DeleteableApiResource,
             CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'orders'

    def coupons(self, id=None):
        if id:
            return OrderCoupons.get(self.get('id'), id, connection=self.get('_connection'))
        else:
            return OrderCoupons.all(self.get('id'), connection=self.get('_connection'))

    def products(self, id=None):
        if id:
            return OrderProducts.get(self.get('id'), id, connection=self.get('_connection'))
        else:
            return OrderProducts.all(self.get('id'), connection=self.get('_connection'))

    def shipments(self, id=None):
        if id:
            return OrderShipments.get(self.get('id'), id, connection=self.get('_connection'))
        else:
            return OrderShipments.all(self.get('id'), connection=self.get('_connection'))

    def shipping_addresses(self, id=None):
        if id:
            return OrderShippingAddresses.get(self.get('id'), id, connection=self.get('_connection'))
        else:
            return OrderShippingAddresses.all(self.get('id'), connection=self.get('_connection'))


class OrderCoupons(ListableApiSubResource):
    resource_name = 'coupons'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderProducts(ListableApiSubResource, CountableApiSubResource):
    resource_name = 'products'
    parent_resource = 'orders'
    parent_key = 'order_id'
    count_resource = 'orders/products'


class OrderShipments(ListableApiSubResource, CreateableApiSubResource,
                     UpdateableApiSubResource, DeleteableApiSubResource,
                     CollectionDeleteableApiSubResource, CountableApiSubResource):
    resource_name = 'shipments'
    parent_resource = 'orders'
    parent_key = 'order_id'
    count_resource = 'orders/shipments'


class OrderShippingAddresses(ListableApiSubResource, CountableApiSubResource):
    resource_name = 'shipping_addresses'
    parent_resource = 'orders'
    parent_key = 'order_id'
    count_resource = 'orders/shipping_addresses'
