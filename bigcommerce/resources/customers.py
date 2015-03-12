from .base import *


class Customers(ListableApiResource, CreateableApiResource,
                UpdateableApiResource, DeleteableApiResource,
                CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'customers'

    def addresses(self, id=None):
        if id:
            return CustomerAddresses.get(self.id, id, connection=self._connection)
        else:
            return CustomerAddresses.all(self.id, connection=self._connection)


class CustomerAddresses(ListableApiSubResource, CreateableApiSubResource,
                        UpdateableApiSubResource, DeleteableApiSubResource,
                        CollectionDeleteableApiSubResource, CountableApiSubResource):
    resource_name = 'addresses'
    parent_resource = 'customers'
    parent_key = 'customer_id'
