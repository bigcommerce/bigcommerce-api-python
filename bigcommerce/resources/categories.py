from .base import *


class Categories(ListableApiResource, CreateableApiResource,
                 UpdateableApiResource, DeleteableApiResource,
                 CollectionDeleteableApiResource):
    resource_name = 'categories'
