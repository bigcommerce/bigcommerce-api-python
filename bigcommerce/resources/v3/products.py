from ..base import *


class Products(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource,
               CollectionDeleteableApiResource, CountableApiResource):
    resource_version = 'v3'
    resource_name = 'catalog/products'

    def bulk_pricing_rules(self, id=None):
        if id:
            return ProductBulkPricingRules.get(self.id, id, connection=self._connection)
        else:
            return ProductBulkPricingRules.all(self.id, connection=self._connection)

    def complex_rules(self, id=None):
        if id:
            return ProductComplexRules.get(self.id, id, connection=self._connection)
        else:
            return ProductComplexRules.all(self.id, connection=self._connection)

    def custom_fields(self, id=None):
        if id:
            return ProductCustomFields.get(self.id, id, connection=self._connection)
        else:
            return ProductCustomFields.all(self.id, connection=self._connection)

    def images(self, id=None):
        if id:
            return ProductImages.get(self.id, id, connection=self._connection)
        else:
            return ProductImages.all(self.id, connection=self._connection)

    def metafields(self, id=None):
        if id:
            return ProductMetafields.get(self.id, id, connection=self._connection)
        else:
            return ProductMetafields.all(self.id, connection=self._connection)

    def modifiers(self, id=None):
        if id:
            return ProductModifiers.get(self.id, id, connection=self._connection)
        else:
            return ProductModifiers.all(self.id, connection=self._connection)

    def videos(self, id=None):
        if id:
            return ProductVideos.get(self.id, id, connection=self._connection)
        else:
            return ProductVideos.all(self.id, connection=self._connection)


class ProductBulkPricingRules(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'XXX'
    parent_resource = Products.resource_name
    key = 'product_id'


class ProductComplexRules(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'XXX'
    parent_resource = Products.resource_name
    parent_key = 'product_id'


class ProductCustomFields(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'XXX'
    parent_resource = Products.resource_name
    parent_key = 'product_id'


class ProductImages(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'XXX'
    parent_resource = Products.resource_name
    parent_key = 'product_id'


class ProductMetafields(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'XXX'
    parent_resource = Products.resource_name
    parent_key = 'product_id'


class ProductModifiers(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'modifiers'
    parent_resource = Products.resource_name
    parent_key = 'product_id'

    def values(self, id=None):
        if id:
            return ProductModifiersValues.get(self.gparent_id(), self.parent_id(), id, connection=self._connection)
        else:
            return ProductModifiersValues.all(self.gparent_id(), self.parent_id(), connection=self._connection)


class ProductModifiersValues(ListableApiSubSubResource, CreateableApiSubSubResource, DeleteableApiSubSubResource):
    resource_version = Products.resource_version
    resource_name = 'values'
    parent_resource = 'modifiers'
    parent_key = 'modifier_id'
    gparent_key = 'product_id'
    gparent_resource=Products.resource_name


class ProductOptions(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'options'
    parent_resource = Products.resource_name
    parent_key = 'product_id'


class ProductOptionsValues(ListableApiSubSubResource, CreateableApiSubSubResource, DeleteableApiSubSubResource):
    resource_version = Products.resource_version
    resource_name = 'values'
    parent_resource = 'options'
    parent_key = 'option_id'
    gparent_key = 'product_id'
    gparent_resource=Products.resource_name

class ProductReviews(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'XXX'
    parent_resource = Products.resource_name
    parent_key = 'product_id'


class ProductVariants(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Products.resource_version
    resource_name = 'variants'
    parent_resource = Products.resource_name
    parent_key = 'product_id'


class ProductVariantsImages(ListableApiSubSubResource, CreateableApiSubSubResource, DeleteableApiSubSubResource):
    resource_version = Products.resource_version
    resource_name = 'images'
    parent_resource = 'variants'
    parent_key = 'variant_id'
    gparent_key = 'product_id'
    gparent_resource=Products.resource_name


class ProductVariantsMetafields(ListableApiSubSubResource, CreateableApiSubSubResource, DeleteableApiSubSubResource):
    resource_version = Products.resource_version
    resource_name = 'metafields'
    parent_resource = 'variants'
    parent_key = 'variant_id'
    gparent_key = 'product_id'
    gparent_resource=Products.resource_name


class ProductVideos(ListableApiSubResource, CountableApiSubResource, 
                    CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = 'v3'
    resource_name = 'videos'
    parent_resource = 'catalog/products'
    parent_key = 'product_id'
    count_resource = 'products/videos'
