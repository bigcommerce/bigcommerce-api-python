from ..base import *


class Products(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource,
               CollectionDeleteableApiResource, CountableApiResource):
    resource_version = 'v3'
    resource_name = 'catalog/products'