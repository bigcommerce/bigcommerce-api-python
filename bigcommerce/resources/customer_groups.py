from .base import *


class CustomerGroups(ListableApiResource, CreateableApiResource,
                     UpdateableApiResource, DeleteableApiResource,
                     CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'customer_groups'
