from base import *

class Orders(ListableApiResource, CreateableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'orders'

    def coupons(self, id=None):
        if id:
            return OrderCoupons.get(self.id, id)
        else:
            return OrderCoupons.all(self.id)

    def products(self, id=None):
        if id:
            return OrderProducts.get(self.id, id)
        else:
            return OrderProducts.all(self.id)

    def shipments(self, id=None):
        if id:
            return OrderShipments.get(self.id, id)
        else:
            return OrderShipments.all(self.id)

    def shipping_addresses(self, id=None):
        if id:
            return OrderShippingAddresses.get(self.id, id)
        else:
            return OrderShippingAddresses.all(self.id)

class OrderCoupons(ListableApiSubResource):
    resource_name = 'coupons'
    parent_resource = 'orders'


class OrderProducts(ListableApiSubResource):
    resource_name = 'products'
    parent_resource = 'orders'


class OrderShipments(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'shipments'
    parent_resource = 'orders'


class OrderShippingAddresses(ListableApiSubResource):
    resource_name = 'shipping_addresses'
    parent_resource = 'orders'

