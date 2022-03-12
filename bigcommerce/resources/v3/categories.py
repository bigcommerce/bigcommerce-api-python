from ..base import *


class Categories(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource,
               CollectionDeleteableApiResource, CountableApiResource):
    resource_version = 'v3'
    resource_name = 'catalog/categories'


# TODO: product sort order
# TODO: images
# TODO: metafields