from mapping import Mapping
from bigcommerce.api.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter
from bigcommerce.api.resources.resource import ResourceObject
from optionsets import OptionSets
from brands import Brands
import subresource

class Products(ResourceObject):
    """
    
    """
    
    # List of known sub resources
    sub_resources = Mapping(brand = Mapping(
                                            klass = Brands,
                                            single = True),
                            configurable_fields = Mapping(),
                            custom_fields = Mapping(),
                            discount_rules = Mapping(),
                            downloads = Mapping(),
                            images = Mapping(klass = subresource.Images),
                            options = Mapping(klass = subresource.ProductOptions),
                            option_set = Mapping(klass = OptionSets, single=True),
                            rules = Mapping(),
                            skus = Mapping(klass = subresource.SKU),
                            tax_class = Mapping(),
                            videos = Mapping(),
                            )
    
    read_only = ["id",
                 "rating_total",
                 "rating_count",
                 "number_sold",
                 "date_created",
                 "date_modified",
                 "date_last_imported",
                 "custom_url"]
    
    @classmethod
    def filter_set(cls):
        return FilterSet(min_id = NumberFilter( info="Minimum id of the product" ),
                      max_id = NumberFilter( info="Minimum id of the product" ),
                      name = StringFilter( info="The product name" ),
                      sku = StringFilter(),
                      description = StringFilter(),
                      condition = StringFilter(),
                      availability = StringFilter(),
                      brand_id = NumberFilter(),
                      min_date_created = DateFilter(),
                      max_date_created = DateFilter(),
                      min_date_modified = DateFilter(),
                      max_date_modified = DateFilter(),
                      min_date_last_imported = DateFilter(),
                      max_date_last_imported = DateFilter(),
                      min_inventory_level = NumberFilter(),
                      max_inventory_level = NumberFilter(),
                      is_visible = BoolFilter(),
                      is_featured = BoolFilter(),
                      min_price = NumberFilter(),
                      max_price = NumberFilter(),
                      min_number_sold = NumberFilter(),
                      max_number_sold = NumberFilter(),
                      ) 
        
    def __repr__(self):
        return "%s- %s" % (self.id, self.name)