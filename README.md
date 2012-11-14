BigCommerce API V2 - Python Client
==================================

This module provides an object-oriented wrapper around the BigCommerce V2 API
for use in Python projects or via the Python shell.

Requirements:

- Python 2.6+


A valid API key is required to authenticate requests. To grant API access for
user, go to Control Panel > Users > Edit User and make sure that the
'Enable the XML API?' checkbox is ticked.

Usage:

```
#!/usr/bin/python
from bigcommerce.api import bigCommerce

api = bigCommerce(STORE_HOST, STORE_TOKEN, STORE_USERID)
    
filters = api.Products.filters()
filters.min_id.set(73873)
	    
# List 10 products starting at offset 10
for product in api.Products.enumerate(start=10, limit=10, query=filters):
	print product.id, product.sku, product.name, product.price
	
```

Features
--------

* All urls to resources are inferred from an initial call to API
* Enumerate multiple pages of resources with "start" and "limit" parameters
* Filtering


Resource Objects
---------------

Information about BigCommerce Resources is specified in the ResourceObjects.  These 
objects also serve as the classes that will be inflated with the results of a query
on that resource type.

ResourceObjects are intended to specify:
* SubResource Types
* Available filters and types
* Read-Only fields (for error checking)
* Fields required for create and update

Product Resource Definition
---------------------------
```
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
```










