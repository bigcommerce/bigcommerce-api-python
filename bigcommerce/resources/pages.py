from .base import *


class Pages(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource,
              CollectionDeleteableApiResource):
    resource_name = 'pages'
