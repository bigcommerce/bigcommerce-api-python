"""
A bunch of classes for each of BigCommerce's resources, individually and
as collections.
"""

import copy
import json

from api import Connection

class ResourceSet(object):
    """
    Base class representing a collection of BigCommerce resources.
    """
    client = Connection()
    resource_class = None
    res_name = "" # this needs to be, e.g., "brands" for brand resources
     
    @classmethod
    def get(cls):
        """Returns list of resources"""
        resource_list = cls.client.get('/{}.json'.format(cls.res_name))
        return [cls.resource_class(res) for res in resource_list]
 
    @classmethod
    def get_by_id(cls, id):
        """Returns an individual resource by given ID"""
        resource = cls.client.get('/{}/{}.json'.format(cls.res_name, id))
        return cls.resource_class(resource)
 
    @classmethod
    def create(cls, fields):
        """
        Creates a new resource, returning its corresponding object.
        Don't include the id field.
        """
        new_obj_data = cls.client.post('/{}.json'.format(cls.res_name), json.dumps(fields))
        return cls.resource_class(new_obj_data)
    
    @classmethod
    def delete_from_id(cls, id):
        cls.client.delete('/{}/{}.json'.format(cls.res_name, id))
 
class Resource(object):
    """
    Base class for an individual resource.
    """
    client = Connection()
    res_name = "" # this needs to be, e.g., "brands" for brand resources
 
    def __init__(self, fields=None):
        self._fields = fields or {} # internal dict for fields
        # __dict__ is used as a staging area for local changes
        # it gets cleared and moved to _fields upon update()
    
    @classmethod
    def get_time(cls):
        return cls.client.get('/time')
        
    def __getattr__(self, attr): # if __dict__ doesn't have it, try _fields
        try:
            return self._fields[attr]
        except KeyError:
            raise AttributeError("No attribute {}".format(attr))
 
    def update(self):
        """Updates local changes to the object."""
        body = copy.deepcopy(self.__dict__)
        if body.has_key('id'):
            del body['id']
        if body.has_key('_fields'): # TODO: inefficient! _fields gets copied and then deleted!
            del body['_fields']
        body = json.dumps(body)
        new_fields = self.client.put('/{}/{}.json'.format(self.res_name, self.id), body)
        # commit changes locally
        self._fields = new_fields
        self.__dict__ = {'_fields' : self._fields}
 
    def delete(self):
        """Deletes the object"""
        self.client.delete('/{}/{}.json'.format(self.res_name, self.id))
  
class Product(Resource):
    res_name = "products"
 
class Products(ResourceSet):
    res_name = "products"
    resource_class = Product
    
class Brand(Resource):
    res_name = "brands"
    
class Brands(ResourceSet):
    res_name = "brands"
    resource_class = Brand
    
class Customer(Resource):
    res_name = "customers"
    
class Customers(ResourceSet):
    res_name = "customers"
    resource_class = Customer
    
class Order(Resource):
    res_name = "orders"
    
class Orders(ResourceSet):
    res_name = "orders"
    resource_class = Order
    
class OptionSet(Resource):
    res_name = "optionsets"
    
class OptionSets(ResourceSet):
    res_name = "optionsets"
    resource_class = OptionSet
    
class Category(Resource):
    res_name = "categories"
    
class Categories(ResourceSet):
    res_name = "categories"
    resource_class = Category
    
class Coupon(Resource):
    res_name = "coupons"
    
class Coupons(ResourceSet):
    res_name = "coupons"
    resource_class = Coupon