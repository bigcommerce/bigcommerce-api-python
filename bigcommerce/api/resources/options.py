from resource import ResourceObject
from OptionValues import OptionValues
from mapping import Mapping
from bigcommerce.api.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter

class Options(ResourceObject):
    """
    
    """
    can_update = True
    read_only = ["id", "type"]
    sub_resources = Mapping(values = Mapping(klass = OptionValues))
    
    @classmethod
    def filter_set(cls):
        return FilterSet(name = StringFilter(),
                      display_name = StringFilter(),
                      type = StringFilter(),
                      )
        
    def __repr__(self):
        return "%s- %s" % (self.id, self.display_name) 