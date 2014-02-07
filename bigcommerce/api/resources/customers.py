from base import *

class Customers(ListableApiResource, CreateableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'customers'

    def addresses(self, id=None):
        if id:
            return CustomerAddresses.get(self.id, id)
        else:
            return CustomerAddresses.all(self.id)

class CustomerAddresses(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'addresses'
    parent_resource = 'customers'

