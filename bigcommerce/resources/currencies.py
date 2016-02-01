from .base import *


class Currencies(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource):
    resource_name = 'currencies'
