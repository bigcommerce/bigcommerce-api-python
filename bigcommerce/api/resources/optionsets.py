from bigcommerce.api.resource import ResourceObject
from OptionValues import OptionValues
from bigcommerce.api.mapping import Mapping
from bigcommerce.api.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter
from OptionSetOptions import OptionSetOptions

class OptionSets(ResourceObject):
    """
    
    """
    can_update = True
    read_only = ["id"]
    
    sub_resources = Mapping(options = Mapping(klass=OptionSetOptions))
    
    def __repr__(self):
        return "%s- %s" % (self.id, self.name)