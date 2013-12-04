import json

from resource import Resource

class SubResource(Resource):
    """
    Base class for resources that are purely subresources.
    These resources should be handled through their corresponding
    ParentResource classes.
    """
    def update(self, options=None): 
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
                                     options)
        # commit changes locally
        self._replace_fields(new_fields)
    
    def delete(self, options=None):
        """
        Deletes this resource from the store.
        Equivalent to GET /resource/subresource/sres_id
        """
        self.client.delete('/{}/{}.json'.format(self.parent_name, 
                                                self.res_name, 
                                                self.id), 
                           options)
    
class CountryState(SubResource):
    res_name = "states"
    parent_name = "countries"
    
class ProductImage(SubResource):
    res_name = "images"
    parent_name = "products"