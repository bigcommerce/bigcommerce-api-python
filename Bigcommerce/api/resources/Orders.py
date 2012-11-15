from Bigcommerce.api.lib.mapping import Mapping
from . import ResourceObject, SubResourceAccessor
import SubResources

class Orders(ResourceObject):
    """
    
    """
    can_update = True
    writeable = ["is_deleted", "status_id"]
    sub_resources = Mapping(
                            shipping_addresses = Mapping(
                                                       klass = SubResources.ShippingAddresses,
                                                       single = False),
                            coupons = Mapping(
                                              klass = SubResources.Coupons,
                                              single = False),
                            products = Mapping(
                                               klass = SubResources.OrderProducts,
                                               single = False)
                            )
    
    
    def __get_shipments(self):
        if self._fields.has_key("shipments"):
            return self._fields["shipments"]
        else:
            url = "%s/shipments" % self.get_url()
            _con = SubResourceAccessor(SubResources.Shipments, url, self._connection, self)
            _list = []
            for sub_res in _con.enumerate():
                _list.append(sub_res)
            
            self._fields["shipments"] = _list 
            return _list
        
    def add_shipment(self, data):
        pass
    
    def __repr__(self):
        return "%s- %s" % (self.id, self.date_created)
    
    shipments = property(fget = __get_shipments)