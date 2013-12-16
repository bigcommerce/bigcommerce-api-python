from mapping import Mapping
from bigcommerce.api.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter
from resource import ResourceObject, SubResourceAccessor
import subresource

class Orders(ResourceObject):
    """
    
    """
    can_update = True
    writeable = ["is_deleted", "status_id"]
    sub_resources = Mapping(
                            shipping_addresses = Mapping(
                                                       klass = subresource.ShippingAddresses,
                                                       single = False),
                            coupons = Mapping(
                                              klass = subresource.Coupons,
                                              single = False),
                            products = Mapping(
                                               klass = subresource.OrderProducts,
                                               single = False)
                            )
    
    @classmethod
    def filter_set(cls):
        return FilterSet(min_id = NumberFilter(info="The minimum id of the order."),
                         max_id = NumberFilter(info="The maximum id of the order."),
                         min_total = NumberFilter(info="The minimum total for the order."),
                         max_total = NumberFilter(info="The maximum total for the order."),
                         customer_id = NumberFilter(info="Filter orders by customers."),
                         status_id = NumberFilter(info="Filter orders by the order status."),
                         is_deleted = BoolFilter(info="Filter orders by the deleted flag."),
                         payment_method = StringFilter(info="Filter orders by payment method."),
                         min_date_created = DateFilter(info="Retrieve all orders created after a specified date."),
                         max_date_created = DateFilter()
                        ) 
    
    
    def __get_shipments(self):
        if self._fields.has_key("shipments"):
            return self._fields["shipments"]
        else:
            url = "%s/shipments" % self.get_url()
            _con = SubResourceAccessor(subresource.Shipments, url, self._connection, self)
            _list = []
            for sub_res in _con.get_all():
                _list.append(sub_res)
            
            self._fields["shipments"] = _list 
            return _list
        
    def add_shipment(self, data):
        pass
    
    def __repr__(self):
        return "%s- %s" % (self.id, self.date_created)
    
    shipments = property(fget = __get_shipments)