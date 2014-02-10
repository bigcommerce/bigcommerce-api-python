from .base import *


class Brands(ListableApiResource, CreateableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'brands'
