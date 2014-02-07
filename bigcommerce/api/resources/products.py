from base import *


class Products(ListableApiResource, CreateableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'products'

    def configurable_fields(self, id=None):
        if id:
            return ProductConfigurableFields.get(self.id, id)
        else:
            return ProductConfigurableFields.all(self.id)

    def custom_fields(self, id=None):
        if id:
            return ProductCustomFields.get(self.id, id)
        else:
            return ProductCustomFields.all(self.id)

    def discount_rules(self, id=None):
        if id:
            return ProductDiscountRules.get(self.id, id)
        else:
            return ProductDiscountRules.all(self.id)

    def images(self, id=None):
        if id:
            return ProductImages.get(self.id, id)
        else:
            return ProductImages.all(self.id)

    def options(self, id=None):
        if id:
            return ProductOptions.get(self.id, id)
        else:
            return ProductOptions.all(self.id)

    def rules(self, id=None):
        if id:
            return ProductRules.get(self.id, id)
        else:
            return ProductRules.all(self.id)

    def skus(self, id=None):
        if id:
            return ProductSkus.get(self.id, id)
        else:
            return ProductSkus.all(self.id)

    def videos(self, id=None):
        if id:
            return ProductVideos.get(self.id, id)
        else:
            return ProductVideos.all(self.id)


class ProductConfigurableFields(ListableApiSubResource, DeleteableApiSubResource):
    resource_name = 'configurable_fields'
    parent_resource = 'products'
    parent_key = 'product_id'


class ProductCustomFields(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'custom_fields'
    parent_resource = 'products'
    parent_key = 'product_id'


class ProductDiscountRules(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'discount_rules'
    parent_resource = 'products'
    parent_key = 'product_id'


class ProductImages(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'images'
    parent_resource = 'products'
    parent_key = 'product_id'


class ProductOptions(ListableApiSubResource):
    resource_name = 'options'
    parent_resource = 'products'
    parent_key = 'product_id'


class ProductRules(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'rules'
    parent_resource = 'products'
    parent_key = 'product_id'


class ProductSkus(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'skus'
    parent_resource = 'products'
    parent_key = 'product_id'


class ProductVideos(ListableApiSubResource):
    resource_name = 'videos'
    parent_resource = 'products'
    parent_key = 'product_id'
