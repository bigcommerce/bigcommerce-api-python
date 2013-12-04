from resource import Resource

class SubResource(Resource):
    """
    Base class for resources that are purely subresources.
    These resources should be handled through their corresponding
    ParentResource classes.
    """
    def update(self): 
        raise Exception("Not implemented for SubResource. Use SubResourceManager of corresponding ParentResource")
    
    def delete(self):
        raise Exception("Not implemented for SubResource. Use SubResourceManager of corresponding ParentResource")
    
class CountryState(SubResource):
    res_name = "states"