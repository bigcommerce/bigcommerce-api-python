from . import ResourceObject
from ..lib.mapping import Mapping

class Customers(ResourceObject):
    """
    
    """
    sub_resources = Mapping(addresses = Mapping())
    
    
    
    