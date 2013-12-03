"""
This module provides an object-oriented wrapper around the BigCommerce V2 API
for use in Python projects or via the Python shell.

The Connection class should mostly be used to configure the connection details
(host, user, api token, etc). Actual interaction with BigCommerce's REST API should
be done through the appropriate resource classes.
 
If anything isn't well supported, the get, post, put, and delete methods of
the class could be used directly:
    all of the methods take a req_path, which corresponds to the URL substring after /api/v2
        (e.g. /products/5.json)
    all of the methods, except delete, return JSON of the response contents,
        typically the resource made/modified/retrieved
"""
 
import requests
import json
import copy

from httpexception import *

# EVERYTHING STILL NEEDS TESTING AAAAAAAAAAAAAAAAAAAAAAAAAAAA
 
API_HOST = 'http://store.mybigcommerce.com'
API_PATH = '/api/v2'
API_USER = 'admin'
API_KEY  = 'yourpasswordhere'
HTTP_PROXY = None
HTTP_PROXY_PORT = 80

class Connection(object):
    """
    Makes connections according to configuration.
    Generally, only host, user, api_key needs to be changed.
    
    Proxies can be defined by doing:
        Connection.proxies = {"http": "http://10.10.1.10:3128",
                              "https": "http://10.10.1.10:1080"}
    
    The four methods corresponding to the http methods return the
    JSON of the response data, or raise an exception if the 
    request failed (see HttpException).
    """
    host      = API_HOST
    base_path = API_PATH
    user      = API_USER
    api_key   = API_KEY
    proxies   = None
    
    json_headers = {'Content-type':'application/json'}
 
    # requests automatically uses keep-alive
    # TODO: let user close the session
 
    @property
    def auth_pair(self):
        return (self.user, self.api_key)
 
    def get(self, req_path):
        full_path = self.host + self.base_path + req_path
        r = requests.get(full_path, auth=self.auth_pair)
        ex = self._check_response(r)
        if ex:
            ex.message = "GET request failed:" + ex.message
            raise ex
        else:
            return r.json()
         
    def delete(self, req_path):
        """
        No return value. Exception if not successful.
        """
        full_path = self.host + self.base_path + req_path
        r = requests.delete(full_path, auth=self.auth_pair)
        ex = self._check_response(r)
        if ex:
            ex.message = "DELETE request failed:" + ex.message
            raise ex
 
    def post(self, req_path, data):
        full_path = self.host + self.base_path + req_path
        r = requests.post(full_path, auth=self.auth_pair, headers=self.json_headers, data=data)
        ex = self._check_response(r)
        if ex:
            ex.message = "POST request failed:" + ex.message
            raise ex
        else:
            return r.json()
         
    def put(self, req_path, data):
        full_path = self.host + self.base_path + req_path
        r = requests.put(full_path, auth=self.auth_pair, headers=self.json_headers, data=data)
        ex = self._check_response(r)
        if ex:
            ex.message = "PUT request failed:" + ex.message
            raise ex
        else:
            return r.json()

#     exception_classes = {501 : UnsupportedRequest,
#                          503 : ServiceUnavailable,
#                          507 : StorageCapacityError,
#                          509 : BandwidthExceeded,
#                          };
    
    def _check_response(self, r):
        """
        Returns an appropriate HttpException object for 
        status codes other than 2xx, and None otherwise.
        """
        ex = None
#         if exception_classes.has_key(r.status_code):
#             ex = exception_classes[r.status_code](str(r.content))
#         elif not r.status_code in (200, 201, 202, 204):
        # the contents of the responses are very descriptive, so I'll just use those
        if not r.status_code in (200, 201, 202, 204):
            if r.status_code >= 500:
                ex = ServerException(str(r.content), r.headers, r.content)
            elif r.status_code >= 400:
                ex = ClientRequestException(str(r.content), r.headers, r.content)
            elif r.status_code >= 300:
                ex = RedirectionException(str(r.content), r.headers, r.content)
        return ex
 
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