from . import ResourceObject
from bigcommerce.api.mapping import Mapping
from bigcommerce.api.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter

class Customers(ResourceObject):
    """
    
    """
    sub_resources = Mapping(addresses = Mapping())
    
    @classmethod
    def filter_set(cls):
        return FilterSet(min_id = NumberFilter( info="Minimum id of the product" ),
                      max_id = NumberFilter( info="Minimum id of the product" ),
                      first_name = StringFilter(),
                      last_name = StringFilter(),
                      company = StringFilter(),
                      email = StringFilter(),
                      phone = StringFilter(),
                      store_credit = NumberFilter(),
                      customer_group_id = NumberFilter(),
                      min_date_created = DateFilter(),
                      max_date_created = DateFilter()
                      ) 
    
    
    def __repr__(self):
        return "%s- %s %s" % (self.id, self.first_name, self.last_name)
    