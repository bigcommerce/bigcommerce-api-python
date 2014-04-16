from . import ResourceObject
from OptionValues import OptionValues
from Bigcommerce.api.lib.mapping import Mapping
from Bigcommerce.api.lib.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter

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