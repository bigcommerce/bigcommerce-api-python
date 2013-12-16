from bigcommerce.api.mapping import Mapping
from resource import ResourceObject
import subresource

class Customers(ResourceObject):
    """
    
    """
    sub_resources = Mapping(addresses = Mapping())