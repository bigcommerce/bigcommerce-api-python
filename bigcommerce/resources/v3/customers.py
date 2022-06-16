from ..base import *


class Customers(ListableApiResource, CreateableApiResource,
                UpdateableApiResource, DeleteableApiResource,
                CollectionDeleteableApiResource, CountableApiResource):

    resource_name = 'customers'
    resource_version = 'v3'

class CustomerAddresses(ListableApiResource, CreateableApiResource, CollectionUpdateableApiResource, DeleteableApiResource):

    resource_name = 'customers/addresses'
    resource_version = 'v3'

class CustomerFormFieldValues(ListableApiResource, UpdateableApiResource):

    resource_name = 'customers/form-field-values'
    resource_version = 'v3'

# TODO: subscribers