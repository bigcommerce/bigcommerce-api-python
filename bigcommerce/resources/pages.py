from .base import *


class Pages(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource,
              CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'pages'
