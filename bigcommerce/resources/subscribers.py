from .base import *


class Subscribers(ListableApiResource, CreateableApiResource,
                UpdateableApiResource, DeleteableApiResource,
                CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'customers/subscribers'
    api_version = 'v3'
