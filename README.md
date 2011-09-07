BigCommerce API V2 - Python Client
==================================

This module provides an object-oriented wrapper around the BigCommerce V2 API
for use in Python projects or via the Python shell.

Requirements:

- Python 2.3+
- python-httplib2

A valid API key is required to authenticate requests. To grant API access for
user, go to Control Panel > Users > Edit User and make sure that the
'Enable the XML API?' checkbox is ticked.

Usage:

```
#!/usr/bin/python
import bigcommerce.api

bigcommerce.api.Connection.host = 'https://store.mybigcommerce.com'
bigcommerce.api.Connection.user = 'admin'
bigcommerce.api.Connection.api_key = '22d05a34ecb25e2d95f5e0208d129b5e1668cade'

products = bigcommerce.api.Products.get()
for p in products:
	print p.name
	print p.price

speakers = bigcommerce.api.Products.get_by_id(22)
speakers.name = "Logitech Pure-Fi Speakers"
speakers.price = "99.95"
speakers.description = "This is a description"
speakers.update()
```

