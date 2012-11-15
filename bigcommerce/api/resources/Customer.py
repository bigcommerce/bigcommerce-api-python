from bigcommerce.api.lib.mapping import Mapping
from . import ResourceObject
import SubResources

class Customers(ResourceObject):
    """
    
    """
    sub_resources = Mapping(addresses = Mapping())