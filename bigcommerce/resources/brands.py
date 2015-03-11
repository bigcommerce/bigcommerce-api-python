from .base import *


class Brands(ListableApiResource, CreateableApiResource,
             UpdateableApiResource, DeleteableApiResource,
             CollectionDeleteableApiResource):
    resource_name = 'brands'
