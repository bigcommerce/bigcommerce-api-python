from .base import *


class Variants(ListableApiResource, CreateableApiSubResource,
                  UpdateableApiSubResource, DeleteableApiSubResource,
                  CollectionDeleteableApiSubResource, CountableApiSubResource):
    resource_name = 'variants'
    parent_resource = 'products'
    parent_key = 'product_id'
    count_resource = 'products/variants'