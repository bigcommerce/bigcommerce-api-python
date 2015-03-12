from .base import *


class Brands(ListableApiResource, CreateableApiResource,
             UpdateableApiResource, DeleteableApiResource,
             CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'brands'
