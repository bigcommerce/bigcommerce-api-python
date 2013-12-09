import json
from resource import Resource

class SubResource(Resource):
    """
    Base class for resources that are purely subresources.
    These resources should be handled through their corresponding
    ParentResource classes.
    """
    def update(self, **options): 
        """
        Updates the given subresource with its local changes.
        Equivalent to PUT /resource/subresource/sres_id
        """
        body = self._copy_dict()
        body = json.dumps(body)
        new_fields = self.client.put('/{}/{}/{}.json'.format(self.parent_name, 
                                                                self.res_name, 
                                                                self.id), 
                                     body,
                                     **options)
        # commit changes locally
        self._replace_fields(new_fields)
    
    def delete(self, **options):
        """
        Deletes this resource from the store.
        Equivalent to GET /resource/subresource/sres_id
        """
        self.client.delete('/{}/{}.json'.format(self.parent_name, 
                                                self.res_name, 
                                                self.id), 
                           **options)
    
class CountryState(SubResource):
    res_name = "states"
    parent_name = "countries"
    
class OptionValue(SubResource):
    res_name = "values"
    parent_name = "options"

class OrderShipment(SubResource):
    res_name = "shipments"
    parent_name = "orders"
    
class OrderShippingAddress(SubResource):
    res_name = "shippingaddresses"
    parent_name = "orders"
    
class ProductSKU(SubResource):
    res_name = "skus"
    parent_name = "products"
 
class ProductConfigurableField(SubResource):
    res_name = "configurablefields"
    parent_name = "products"
    
class ProductCustomField(SubResource):
    res_name = "customfields"
    parent_name = "products"
    
class ProductDiscountRule(SubResource):
    res_name = "discountrules"
    parent_name = "products"
    
class ProductImage(SubResource):
    res_name = "images"
    parent_name = "products"
    
class ProductRule(SubResource):
    res_name = "rules"
    parent_name = "products"
    
class ProductVideo(SubResource):
    res_name = "productvideos"
    parent_name = "products"
    
class ShippingMethod(SubResource):
    res_name = "methods"
    parent_name = "shipping"