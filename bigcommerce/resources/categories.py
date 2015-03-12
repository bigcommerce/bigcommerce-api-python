from .base import *


class Categories(ListableApiResource, CreateableApiResource,
                 UpdateableApiResource, DeleteableApiResource,
                 CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'categories'
