from ..base import *


class Brands(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource,
               CollectionDeleteableApiResource, CountableApiResource):
    resource_version = 'v3'
    resource_name = 'catalog/brands'

    def images(self, id=None):
        if id:
            return BrandImages.get(self.id, id, connection=self._connection)
        else:
            return BrandImages.all(self.id, connection=self._connection)

    def metafields(self, id=None):
        if id:
            return BrandMetafields.get(self.id, id, connection=self._connection)
        else:
            return BrandMetafields.all(self.id, connection=self._connection)


class BrandImages(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Brands.resource_version
    resource_name = 'XXX'
    parent_resource = Brands.resource_name
    parent_key = 'brand_id'


class BrandMetafields(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Brands.resource_version
    resource_name = 'XXX'
    parent_resource = Brands.resource_name
    parent_key = 'brand_id'
