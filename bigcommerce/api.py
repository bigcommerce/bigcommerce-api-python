import urllib
import httplib2
import base64
import json

API_HOST = 'http://bigcommerce.local'
API_PATH = '/api/v1'
API_USER = 'admin'
API_KEY  = 'apikey'

class Connection(object):
	host      = API_HOST
	base_path = API_PATH
	user 	  = API_USER
	api_key   = API_KEY

	def fetch_obj(self, method, path, data=None):
		response, content = self.fetch(method, path, data)
		if response.status == 200 or response.status == 201:
			return json.loads(content)
		else:
			print response
			raise Exception(response.status)
		

	def fetch(self, method, path, data=None):
		http = httplib2.Http()
		auth = base64.encodestring(self.user + ':' + self.api_key)
		url = self.host + self.base_path + path      	
		return http.request(url, method, headers = {'Authorization' : 'Basic ' + auth, 'Accept' : 'application/json', 'Content-Type' : 'application/json'}, body=data)

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
		return self.client.fetch_obj('GET', '/time')

class Products(Resource):
	"""The collection of products in a store"""

	@classmethod
	def get(self):
		"""Returns list of products"""
		products_list = self.client.fetch_obj('GET', '/products')
		return [Product(product) for product in products_list]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual product by given ID"""
		product = self.client.fetch_obj('GET', '/products/' + str(id))
		return Product(product)

class Product(Resource):
	"""An individual product"""

	def update(self):
		"""Updates local changes to the product"""
		body = json.dumps(self.__dict__)
		product = self.client.fetch_obj('PUT', '/products/' + str(self.id), body)

	def delete(self):
		"""Deletes the product"""
		response, content = self.client.fetch('DELETE', '/products/' + str(self.id))

class Brands(Resource):
	"""Brands collection"""
	
	@classmethod
	def get(self):
		"""Returns list of brands"""
		brands_list = self.client.fetch_obj('GET', '/brands')
		return [Brand(brand) for brand in brands_list]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual brand by given ID"""
		product = self.client.fetch_obj('GET', '/brands/' + str(id))
		return Product(product)

class Brand(Resource):
	"""An individual brand"""

	def create(self):
		"""Creates a new brand"""
		body = json.dumps(self.__dict__)
		brand = self.client.fetch_obj('PUT', '/brands', body)

	def update(self):
		"""Updates local changes to the brand"""
		body = json.dumps(self.__dict__)
		brand = self.client.fetch_obj('PUT', '/brands/' + str(self.id), body)
		print brand['name']

	def delete(self):
		"""Deletes the brand"""
		response, content = self.client.fetch('DELETE', '/brands/' + str(self.id))

class Customers(Resource):
	"""Customers collection"""

	@classmethod
	def get(self):
		"""Returns list of customers"""
		customers = self.client.fetch_obj('GET', '/customers')
		return [Customer(customer) for customer in customers]

	@classmethod
	def get_by_id(self, id):
		"""Returns an individual customer by given ID"""
		customer = self.client.fetch_obj('GET', '/customers/' + str(id))
		return Customer(customer)

class Customer(Resource):
	"""An individual customer"""

	def create(self):
		"""Creates a new customer"""
		body = json.dumps(self.__dict__)
		customer = self.client.fetch_obj('PUT', '/customers', body)

	def update(self):
		"""Updates local changes to the customer"""
		body = json.dumps(self.__dict__)
		customer = self.client.fetch_obj('PUT', '/customers/' + str(self.id), body)

	def delete(self):
		"""Deletes the customer"""
		response, content = self.client.fetch('DELETE', '/customers/' + str(self.id))
	
