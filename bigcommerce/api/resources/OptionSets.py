from . import ResourceObject
from OptionValues import OptionValues
from Bigcommerce.api.lib.mapping import Mapping
from Bigcommerce.api.lib.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter
from OptionSetOptions import OptionSetOptions

class OptionSets(ResourceObject):
    """
    
    """
    can_update = True
    read_only = ["id"]
    
    sub_resources = Mapping(options = Mapping(klass=OptionSetOptions))
    
    def __repr__(self):
        return "%s- %s" % (self.id, self.name)