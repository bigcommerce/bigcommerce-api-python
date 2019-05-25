from .base import *


class Variants(ListableApiResource, CreateableApiResource,
                 UpdateableApiResource, DeleteableApiResource,
                 CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'variants'
