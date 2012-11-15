from . import ResourceObject
from bigcommerce.api.lib.mapping import Mapping
from bigcommerce.api.lib.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter


class ShippingAddresses(ResourceObject):
    pass


class Coupons(ResourceObject):
    pass


class OrderProducts(ResourceObject):
    sub_resources = Mapping(
                            applied_discounts = Mapping(),
                            product_options = Mapping(),
                            configurable_fields = Mapping())
    
    


class Shipments(ResourceObject):
    can_update = True
    read_only = ["id", "date_created", "customer_id", "shipping_method", "items"]
    sub_resource = Mapping(billing_address = Mapping(single=True),
                           shipping_address = Mapping(single=True),
                           items = Mapping())
    pass


class ConfigurableFields(ResourceObject):
    pass



class SKU(ResourceObject):
    sub_resources = Mapping(options = Mapping())
    read_only = ["id","product_id"]
    can_update = True
    
    @classmethod
    def filter_set(cls):
        return FilterSet(min_id = NumberFilter( info="Minimum id of the product" ),
                      max_id = NumberFilter( info="Minimum id of the product" ),
                      sku = StringFilter(),
                      upc = StringFilter(),
                      min_inventory_level = NumberFilter(),
                      max_inventory_level = NumberFilter(),
                      inventory_warning_level = NumberFilter(),
                      bin_picking_number = NumberFilter(),
                      ) 
    
class ProductOptions(ResourceObject):
    pass


class States(ResourceObject):
    @classmethod
    def filter_set(cls):
        return FilterSet(state = StringFilter(),
                      state_abbreviations = StringFilter()
                      ) 
    

class Images(ResourceObject):
    can_update = True
    read_only = ["id","product_id","date_created"]
    