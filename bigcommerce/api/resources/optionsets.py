from bigcommerce.api.resources import ResourceObject
#from optionvalues import OptionValues 
from mapping import Mapping
from bigcommerce.api.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter
from optionsetoptions import OptionSetOptions

class OptionSets(ResourceObject):
    """
    
    """
    can_update = True
    read_only = ["id"]
    
    sub_resources = Mapping(options = Mapping(klass=OptionSetOptions))
    
    def __repr__(self):
        return "%s- %s" % (self.id, self.name)