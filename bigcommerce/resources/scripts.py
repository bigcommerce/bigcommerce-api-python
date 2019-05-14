from .base import *


class Scripts(ListableApiResource, CreateableApiResource,
                UpdateableApiResource, DeleteableApiResource,
                CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'content/scripts'
    api_version = 'v3'
