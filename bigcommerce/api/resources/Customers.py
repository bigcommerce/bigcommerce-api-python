from . import ResourceObject
from bigcommerce.api.lib.mapping import Mapping

class Customers(ResourceObject):
    """
    
    """
    sub_resources = Mapping(addresses = Mapping())
    
    
    
    