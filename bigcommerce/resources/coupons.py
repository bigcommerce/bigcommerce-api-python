from .base import *


class Coupons(ListableApiResource, CreateableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'coupons'
