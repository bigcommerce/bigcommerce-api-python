"""
This module provides an object-oriented wrapper around the BigCommerce V2 API
for use in Python projects or via the Python shell.

"""

import httplib2
import base64
import json

API_HOST = 'http://store.mybigcommerce.com'
API_PATH = '/api/v2'
API_USER = 'admin'
API_KEY  = 'yourpasswordhere'

class Connection(object):
	host      = API_HOST
	base_path = API_PATH
	user 	  = API_USER
	api_key   = API_KEY

	def handle_response(self, response):
		pass

	def request_json(self, method, path, data=None):
		response, content = self.request(method, path, data)
		if response.status == 200 or response.status == 201:
			return json.loads(content)
		else:
			print response
			raise Exception(response.status)

	def build_request_headers(self):
		auth = base64.b64encode(self.user + ':' + self.api_key)
		return { 'Authorization' : 'Basic ' + auth, 'Accept' : 'application/json' }

	def request(self, method, path, body=None):
		http = httplib2.Http()
		url = self.host + self.base_path + path
		headers = self.build_request_headers()
		if body: headers['Content-Type'] = 'application/json'
		return http.request(url, method, headers=headers, body=body)

class Resource(object):
	"""Base class representing BigCommerce resources"""

	client = Connection()

	def __init__(self, fields={}):
		self.__dict__ = fields

class Time(Resource):
	"""Tests the availability of the API."""

	@classmethod
	def get(self):
		"""Returns the current time stamp of the BigCommerce store."""
		return self.client.request_json('GET', '/time')

class Products(Resource):
	"""The collection of products in a store"""

	@classmethod
	def get(self):
		"""Returns list of products"""
		products_list = self.client.request_json('GET', '/products')
		return [Product(product) for product in products_list]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual product by given ID"""
		product = self.client.request_json('GET', '/products/' + str(id))
		return Product(product)

class Product(Resource):
	"""An individual product"""

	def update(self):
		"""Updates local changes to the product"""
		body = json.dumps(self.__dict__)
		product = self.client.request_json('PUT', '/products/' + str(self.id), body)

	def delete(self):
		"""Deletes the product"""
		response, content = self.client.request('DELETE', '/products/' + str(self.id))

class Brands(Resource):
	"""Brands collection"""

	@classmethod
	def get(self):
		"""Returns list of brands"""
		brands_list = self.client.request_json('GET', '/brands')
		return [Brand(brand) for brand in brands_list]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual brand by given ID"""
		product = self.client.request_json('GET', '/brands/' + str(id))
		return Product(product)

class Brand(Resource):
	"""An individual brand"""

	def create(self):
		"""Creates a new brand"""
		body = json.dumps(self.__dict__)
		brand = self.client.request_json('PUT', '/brands', body)

	def update(self):
		"""Updates local changes to the brand"""
		body = json.dumps(self.__dict__)
		brand = self.client.request_json('PUT', '/brands/' + str(self.id), body)
		print brand['name']

	def delete(self):
		"""Deletes the brand"""
		response, content = self.client.request('DELETE', '/brands/' + str(self.id))

class Customers(Resource):
	"""Customers collection"""

	@classmethod
	def get(self):
		"""Returns list of customers"""
		customers = self.client.request_json('GET', '/customers')
		return [Customer(customer) for customer in customers]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual customer by given ID"""
		customer = self.client.request_json('GET', '/customers/' + str(id))
		return Customer(customer)

class Customer(Resource):
	"""An individual customer"""

	def create(self):
		"""Creates a new customer"""
		body = json.dumps(self.__dict__)
		customer = self.client.request_json('PUT', '/customers', body)

	def update(self):
		"""Updates local changes to the customer"""
		body = json.dumps(self.__dict__)
		customer = self.client.request_json('PUT', '/customers/' + str(self.id), body)

	def delete(self):
		"""Deletes the customer"""
		response, content = self.client.request('DELETE', '/customers/' + str(self.id))

class Orders(Resource):
	"""Orders collection"""

	@classmethod
	def get(self):
		"""Returns list of orders"""
		orders = self.client.request_json('GET', '/orders')
		return [Order(order) for order in orders]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual order by given ID"""
		order = self.client.request_json('GET', '/orders/' + str(id))
		return Order(order)

class Order(Resource):
	"""An individual order"""

	def create(self):
		"""Creates a new order"""
		body = json.dumps(self.__dict__)
		order = self.client.request_json('PUT', '/orders', body)

	def update(self):
		"""Updates local changes to the order"""
		body = json.dumps(self.__dict__)
		order = self.client.request_json('PUT', '/orders/' + str(self.id), body)

	def delete(self):
		"""Deletes the order"""
		response, content = self.client.request('DELETE', '/orders/' + str(self.id))

class OptionSets(Resource):
	"""Option sets collection"""

	@classmethod
	def get(self):
		"""Returns list of option sets"""
		optionsets = self.client.request_json('GET', '/optionsets')
		return [OptionSet(optionset) for optionset in optionsets]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual option set by given ID"""
		optionset = self.client.fetch_obj('GET', '/optionsets/' + str(id))
		return OptionSet(optionset)

class OptionSet(Resource):
	"""An individual option set"""

	def create(self):
		"""Creates a new option set"""
		body = json.dumps(self.__dict__)
		optionset = self.client.request_json('PUT', '/optionsets', body)

	def update(self):
		"""Updates local changes to the option set"""
		body = json.dumps(self.__dict__)
		optionset = self.client.request_json('PUT', '/optionsets/' + str(self.id), body)

	def delete(self):
		"""Deletes the option set"""
		response, content = self.client.request('DELETE', '/optionsets/' + str(self.id))

class Categories(Resource):
	"""Categories collection"""

	@classmethod
	def get(self):
		"""Returns list of categories"""
		categories = self.client.request_json('GET', '/categories')
		return [Category(category) for category in categories]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual category by given ID"""
		category = self.client.request_json('GET', '/categories/' + str(id))
		return Category(category)

class Category(Resource):
	"""An individual category"""

	def create(self):
		"""Creates a new category"""
		body = json.dumps(self.__dict__)
		category = self.client.request_json('PUT', '/categories', body)

	def update(self):
		"""Updates local changes to the category"""
		body = json.dumps(self.__dict__)
		category = self.client.request_json('PUT', '/categories/' + str(self.id), body)

	def delete(self):
		"""Deletes the category"""
		response, content = self.client.request('DELETE', '/categories/' + str(self.id))

