from . import ResourceObject
from ..lib.mapping import Mapping

class ShippingAddresses(ResourceObject):
    pass

class Coupons(ResourceObject):
    pass

class OrderProducts(ResourceObject):
    pass

class Shipments(ResourceObject):
    pass

class ConfigurableFields(ResourceObject):
    pass

class OptionSets(ResourceObject):
    sub_resources = Mapping(options = Mapping())

class SKU(ResourceObject):
    sub_resources = Mapping(options = Mapping())
    
class ProductOptions(ResourceObject):
    pass