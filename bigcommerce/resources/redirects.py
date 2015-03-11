from .base import *


class Redirects(ListableApiResource, CreateableApiResource,
                UpdateableApiResource, DeleteableApiResource,
                CollectionDeleteableApiResource):
    resource_name = 'redirects'
