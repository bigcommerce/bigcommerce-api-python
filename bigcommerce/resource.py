"""
A bunch of classes for each of BigCommerce's resources, individually and
as collections.

Supports filter options as dictionaries, e.g.
    someresourceset.get(options={'limit' : 5, 'page' : 2})
See the BigCommerce resources index documentation for available filter fields.
    http://developer.bigcommerce.com/docs/api/v2/resources
"""

import json
from connection import Connection

class ResourceSet(object):
    """
    Base class representing a collection of BigCommerce resources.
    """
    client = Connection
    resource_class = None
    res_name = "" # this needs to be, e.g., "brands" for brand resources
     
    @classmethod
    def count(cls):
        return cls.client.get('/{}/count.json'.format(cls.res_name))['count']
     
    @classmethod
    def get(cls, **options):
        """
        Returns list of resources.
        """
        req = '/{}.json'.format(cls.res_name)
        resource_list = cls.client.get(req, **options)
        return [cls.resource_class(res) for res in resource_list] if resource_list else None
 
    @classmethod
    def get_by_id(cls, id, **options):
        """Returns an individual resource by given ID"""
        req = '/{}/{}.json'.format(cls.res_name, id)
        resource = cls.client.get(req, **options)
        return cls.resource_class(resource) if resource else None
 
    @classmethod
    def create(cls, fields, **options):
        """
        Creates a new resource, returning its corresponding object.
        Don't include the id field.
        Fails (raises an exception) if mandatory fields are missing. See
        resource documentation for which fields are required.
        """
        new_obj_data = cls.client.post('/{}.json'.format(cls.res_name), json.dumps(fields), **options)
        return cls.resource_class(new_obj_data) if new_obj_data else None
    
    @classmethod
    def delete_from_id(cls, id, **options):
        cls.client.delete('/{}/{}.json'.format(cls.res_name, id), **options)
 
class Resource(object):
    """
    Base class for an individual resource.
    """
    client = Connection
    res_name = "" # this needs to be, e.g., "brands" for brand resources
 
    def __init__(self, fields=None):
        """
        This constructor should only be used with a dict of fields 
        retrieved from a store. 
        If you want to create a new resource, use
        the corresponding ResourceSet.create method.
        """
        self._fields = fields or {} # internal dict for fields
        # __dict__ is used as a staging area for local changes
        # it gets cleared and moved to _fields upon update()
    
    @classmethod
    def get_time(cls): # TODO: format? or at least note how to
        return cls.client.get('/time')
        
    def __getattr__(self, attr): # if __dict__ doesn't have it, try _fields
        try:
            return self._fields[attr]
        except KeyError:
            raise AttributeError("No attribute {}".format(attr))

    def delete(self, **options):
        """Deletes this object"""
        self.client.delete('/{}/{}.json'.format(self.res_name, self.id), **options)
 
    def update(self, **options):
        """Updates local changes to the object."""
        body = self._copy_dict()
        body = json.dumps(body)
        new_fields = self.client.put('/{}/{}.json'.format(self.res_name, self.id), body, **options)
        # commit changes locally
        self._replace_fields(new_fields)
        
    def _copy_dict(self):
        copy_d = self.__dict__.copy()
        if copy_d.has_key('id'):
            del copy_d['id']
        del copy_d['_fields']
        return copy_d

    def _replace_fields(self, new_fields):
        self._fields = new_fields if new_fields else {}
        self.__dict__ = {'_fields' : self._fields}
 
class ParentResource(Resource):
    """
    A Resource class that has subresources. 

    Implements subresource related operations that do not
    require a specific instance of a ParentResource.
    Contains a SubResourceManager for operations that do.
    """
    # in future, should allow the get methods to take names of the subresources, rather than just class
    # also in future - should move some of these methods to mixins, or otherwise restrict them
    # for resources that do not support some methods ...
    
    def __init__(self, fields=None):
        super(ParentResource, self).__init__(fields)
        self.subresources = SubResourceManager(self)

    @classmethod
    def count_all(cls, sres_class):
        """
        Number of all subresources of type sres_class.
        GET /resource/subresource/count
        """
        req_str = '/{}/{}/count.json'
        return cls.client.get(req_str.format(cls.res_name, 
                                             sres_class.resname))['count']
                                             
    @classmethod
    def get_sres_by_id(cls, sres_class, id, **options):
        """
        Returns an individual subresource by given ID.
        Equivalent to GET /resource/subresource/sres_id
        """
        sres_name = sres_class.res_name
        resource = self.client.get('/{}/{}/{}.json'.format(self.res_name, sres_name, id), 
                                   **options)
        return sres_class(resource) if resource else None
               
    @classmethod                                  
    def get_all_sres(cls, sres_class, **options):
        """
        List of subresources of type sres_class, up to default limit (can be specified in options).
        GET /resource/subresource
        """ 
        resource_list = cls.client.get('/{}/{}.json'.format(cls.res_name, sres_class.res_name), **options)
        return [sres_class(res) for res in resource_list] if resource_list else None
    
    def _copy_dict(self):
        copy_d = super(ParentResource, self)._copy_dict()
        del copy_d['subresources']
        return copy_d
    
    def _replace_fields(self, new_fields):
        self._fields = new_fields
        self.__dict__ = {'_fields' : self._fields,
                         'subresources' : self.subresources}

class SubResourceManager(object):
    """
    Handles the subresources of a specific instance of a ParentResource.
    
    Uses very similar interface to ResourceSet,
    but requires a subresource class or instance to be passed in as argument.
    
    Not all operations are supported by all resources/subresources.
    Refer to the BigCommerce resources documentation if unsure.
    
    Currently, all methods are available for all parent resources. There is
    no guarentee that all methods will be supported, in which case a 400 or 501
    exception may be raised.
    """
    
    def __init__(self, parent_res):
        self._res = parent_res
    
    @property
    def id(self):
        return self._res.id
    
    @property
    def res_name(self):
        return self._res.res_name
    
    @property
    def client(self):
        return self._res.client
    
    def create(self, sres_class, fields, **options):
        """
        Creates a new resource, returning its corresponding object.
        Don't include the id field.
        Equivalent to POST /resource/res_id/subresource
        """
        sres_name = sres_class.res_name
        new_obj_data = self.client.post('/{}/{}/{}.json'.format(self.res_name, self.id, sres_name),
                                       json.dumps(fields), 
                                       **options)
        return sres_class(new_obj_data) if new_obj_data else None
    
    def count(self, sres):
        """
        Returns number of subresources, corresponding to sres, related
        to this object.
        """
        sres_name = sres.res_name
        req_str = '/{}/{}/{}/count.json'
        return self.client.get(req_str.format(self.res_name, self.id, sres_name))['count']
     
    def get(self, sres_class, **options):
        """
        Returns list of subresources related to this object (up to limit, 
        default or specified).
        Equivalent to GET resource/res_id/subresource
        
        Can be used like get_by_id if id is given.
        """
        sres_name = sres_class.res_name
        resource_list = self.client.get('/{}/{}/{}.json'.format(self.res_name, self.id, sres_name),
                                        **options)
        return [sres_class(res) for res in resource_list] if resource_list else None
 
    def get_by_id(self, sres_class, id, **options):
        """
        Returns an individual subresource of this object by given ID.
        Equivalent to GET /resource/res_id/subresource/sres_id
        """
        sres_name = sres_class.res_name
        resource = self.client.get('/{}/{}/{}/{}.json'.format(self.res_name, self.id, sres_name, id),
                                   **options)
        return sres_class(resource) if resource else None
    
    def delete_all(self, sres_class, **options):
        """
        DELETE /resource/res_id/subresource
        """
        self.client.delete('/{}/{}/{}.json'.format(self.res_name, self.id, sres_class.res_name),
                           **options)
        
    def delete(self, sres, **options):
        """
        DELETE /resource/res_id/subresource/sres_id
        """
        self.client.delete('/{}/{}/{}/{}.json'.format(self.res_name, self.id, sres.res_name, sres.id),
                           **options)
        
    def update(self, sres, **options):
        """
        Updates the given subresource with its local changes.
        Equivalent to PUT /resource/res_id/subresource/sres_id
        """
        body = sres._copy_dict()
        body = json.dumps(body)
        new_fields = self.client.put('/{}/{}/{}/{}.json'.format(self.res_name, 
                                                                self.id, 
                                                                sres.res_name, 
                                                                sres.id), 
                                     body,
                                     **options)
        # commit changes locally
        sres._replace_fields(new_fields)

# Resources and ResourceSets

class Brand(Resource):
    res_name = "brands"
    
class Brands(ResourceSet):
    res_name = "brands"
    resource_class = Brand

class Category(Resource):
    res_name = "categories"
    
class Categories(ResourceSet):
    res_name = "categories"
    resource_class = Category
    
class OrderStatus(Resource):
    res_name = "orderstatuses"
    
class OrderStatuses(ResourceSet):
    res_name = "orderstatuses"
    resource_class = OrderStatus

class CustomerGroup(Resource):
    res_name = "customer_groups"
    
class CustomerGroups(ResourceSet):
    res_name = "customer_groups"
    resource_class = CustomerGroup

class Coupon(Resource):
    res_name = "coupons"
    
class Coupons(ResourceSet):
    res_name = "coupons"
    resource_class = Coupon

class Store(Resource):
    res_name = "store"
    
class Stores(ResourceSet):
    """Only supports GET /store.json, according to documentation."""
    res_name = "store"
    resource_class = Store

class Country(ParentResource):
    res_name = "countries"
        
class Countries(ResourceSet):
    res_name = "countries"
    resource_class = Country

class Customer(ParentResource):
    res_name = "customers"
    
class Customers(ResourceSet):
    res_name = "customers"
    resource_class = Customer
    
class Option(ParentResource):
    res_name = "options"
    
class Options(ResourceSet):
    res_name = "options"
    resource_class = Option

class OptionSet(ParentResource):
    res_name = "optionsets"
    
class OptionSets(ResourceSet):
    res_name = "optionsets"
    resource_class = OptionSet

class Order(ParentResource):
    res_name = "orders"
    
class Orders(ResourceSet):
    res_name = "orders"
    resource_class = Order

class Product(ParentResource):
    res_name = "products"
 
class Products(ResourceSet):
    res_name = "products"
    resource_class = Product
    
class Redirect(Resource):
    res_name = "redirects"
    
class Redirects(ResourceSet):
    res_name = "redirects"
    resource_class = Redirect
    
class Shipping(ParentResource):
    """Only GET"""
    res_name = "shipping"

# class Shippings(ResourceSet):
#     """
#     An actual "Shipping" resource does not appear to exist.
#     The resource is actually shipping methods - use Shipping.get_all_sres
#     and other methods to interact.
#     """
#     res_name = "shipping"
#     resource_class = Shipping