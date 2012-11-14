from . import ResourceObject
from ..lib.mapping import Mapping
from OptionValues import OptionValues

class Options(ResourceObject):
    """
    
    """
    sub_resources = Mapping(values = Mapping(klass = OptionValues))