from ..lib.mapping import Mapping
from ..lib.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter
from . import ResourceObject
from Brands import Brands
import SubResources

class Products(ResourceObject):
    """
    
    """
    sub_resources = Mapping(brand = Mapping(
                                            klass = Brands,
                                            single = True),
                            configurable_fields = Mapping(),
                            custom_fields = Mapping(),
                            discount_rules = Mapping(),
                            downloads = Mapping(),
                            images = Mapping(),
                            options = Mapping(klass = SubResources.ProductOptions),
                            option_set = Mapping(klass = SubResources.OptionSets, single=True),
                            rules = Mapping(),
                            skus = Mapping(klass = SubResources.SKU),
                            tax_class = Mapping(),
                            videos = Mapping(),
                            )
    
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