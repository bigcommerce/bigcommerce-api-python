BigCommerce API V2 - Python Client
==================================

This module provides a lightweight object-oriented wrapper around the BigCommerce V2 API
for use in Python projects or via the Python shell. 

Requirements:

- Python 2.6+
- requests

For a given user, a valid API key is required to authenticate requests. To grant 
API access for user, go to Control Panel > Users > Edit User and make sure that the
'Enable the API' checkbox is ticked.

Usage:

The API focuses on the subclasses of Resource and Resources. They all share the same functionality
(except for subobjects (not yet implemented)), so the examples below should be applicable to all
resources.

The resources are:
    Product
    Brand
    Customer
    screw it update later

Setup:
```
from bigcommerce.connection import Connection 
import bigcommerce.resource as resource

Connection.host = YOUR_STORE    # eg. 'mystore.bigcommerce.com
Connection.user = USER          # eg. 'admin'
Connection.api_key = API_KEY    # eg. 'a2e777fbb2d98fd04461d700463a8ed71782e475'
```

Retrieving:
```
products = resource.Products.get()
for p in products:
    print p.id
    print p.name
    print p.price
```

Updating:
```
speakers = Products.get_by_id(32)
speakers.name = "Logitech Pure-Fi Speakers"
speakers.price *= 1.5
speakers.description = "This description sucks"
speakers.update()   # commit local changes
```

Creating:
```
new_c = Coupons.create({'name' : "70% off order total", 
                        'amount' : 70.00, 
                        'code' : "HT75", 
                        'type' : "percentage_discount", 
                        'applies_to' : {'entity' : "products", 'ids' : [32]}})
```
The create method saves the resource to the store server (equivalent to a POST request), and
returns the corresponding resource object (Coupon in this case)

Deleting:
```
Coupons.delete_from_id(new_c.id)

# OR

new_c.delete()
```

Exceptions:


To Do:

- support for sub-objects
- support for additional options (query strings)