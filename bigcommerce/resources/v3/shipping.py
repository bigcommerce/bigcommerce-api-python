from ..base import *


# TODO: test
class ShippingProductsCustomsInformation(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'shipping/products/customs-information'

    # TODO: add subresource function
