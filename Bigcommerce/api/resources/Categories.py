from . import ResourceObject
from Bigcommerce.api.lib.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter

class Categories(ResourceObject):
    """
    
    """
    can_update = True
    read_only = ["id", "parent_category_list"]
    
    @classmethod
    def filter_set(cls):
        return FilterSet(min_id = NumberFilter( info="Minimum id of the product" ),
                      max_id = NumberFilter( info="Minimum id of the product" ),
                      name = StringFilter(),
                      parent_id = NumberFilter(),
                      is_visible = BoolFilter(),
                      ) 
        
    def __repr__(self):
        return "%s- %s" % (self.id, self.name)
    
    
    
    