from .base import *


class Coupons(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource,
              CollectionDeleteableApiResource):
    resource_name = 'coupons'
