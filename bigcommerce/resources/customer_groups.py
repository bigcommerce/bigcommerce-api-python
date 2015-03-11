from .base import *


class CustomerGroups(ListableApiResource, CreateableApiResource,
                     UpdateableApiResource, DeleteableApiResource,
                     CollectionDeleteableApiResource):
    resource_name = 'customer_groups'
