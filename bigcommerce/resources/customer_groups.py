from .base import *


class CustomerGroups(ListableApiResource, CreateableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'customer_groups'
