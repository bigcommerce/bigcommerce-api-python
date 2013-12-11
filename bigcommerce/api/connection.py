"""
Connection Module

Handles put and get operations to the Bigcommerce REST API
"""

import urllib # only used for urlencode querystr
import logging
import simplejson
from pprint import pformat # only used once, in __load_urls

import requests

log = logging.getLogger("BigCommerce.con")

class HttpException(Exception):
    """
    Class for representing http errors. Contains headers and content of
    the error response.
    """
    def __init__(self, msg, status_code, headers=None, content=None):
        super(Exception, self).__init__(msg)
        self.status_code = status_code
        self.headers = headers
        self.content = content
  
# 204
class EmptyResponseWarning(HttpException): pass
    
# 4xx codes
class ClientRequestException(HttpException): pass
# class Unauthorised(ClientRequestException): pass
# class AccessForbidden(ClientRequestException): pass
# class ResourceNotFound(ClientRequestException): pass
# class ContentNotAcceptable(ClientRequestException): pass

# 5xx codes
class ServerException(HttpException): pass
# class ServiceUnavailable(ServerException): pass
# class StorageCapacityError(ServerException): pass
# class BandwidthExceeded(ServerException): pass

# 405 and 501 - still just means the client has to change their request
# class UnsupportedRequest(ClientRequestException, ServerException): pass

# 3xx codes
class RedirectionException(HttpException): pass

class Connection():
    """
    Connection class manages the connection to the Bigcommerce REST API.
    """
    
    def __init__(self, host, base_url, auth): # auth already base64 encoded
        """
        Constructor
        
        On creation, an initial call is made to load the mappings of resources to URLs
        """
        self.host = host
        self.base_url = base_url
        self.auth = auth
        
        log.info("API Host: %s/%s" % (self.host, self.base_url))
        log.debug("Accepting json, auth: Basic %s" % self.auth)
        self.__headers = {"Authorization": "Basic %s" % self.auth,
                        "Accept": "application/json"}
        
        self.__resource_meta = {}
        self.__load_urls()
        
        
    def meta_data(self):
        """
        Return a string representation of resource-to-url mappings 
        """
        return simplejson.dumps(self.__resource_meta)    
        
        
    def __load_urls(self):
        """
        Hit the base url and get the urls and resources from 
        the server
        """
        self.__resource_meta = self.get()
        log.debug("Registry")
        log.debug(pformat(self.__resource_meta))
        
    def get_url(self, resource_name):
        """
        Lookup the "url" for the resource name from the internally stored resource mappings
        """
        return self.__resource_meta.get(resource_name,{}).get("url", None)
    
    def get_resource_url(self, resource_name):
        """
        Lookup the "resource" for the resource name from the internally stored resource mappings
        """
        return self.__resource_meta.get(resource_name,{}).get("resource", None)

    def full_path(self, url):
        return "https://" + self.host + self.base_url + url
    
    def get(self, url="", query={}):
        """
        Perform the GET request and return the parsed results
        """
        qs = urllib.urlencode(query)
        if qs:
            qs = "?%s" % qs
        url = "%s%s" % (url, qs)
        
        log.debug("GET %s" % (url))
        
        response = requests.get(self.full_path(url), headers=self.__headers)
        
        log.debug("GET %s status %d" % (url,response.status_code))
        
        return self._handle_response(url, response)
        
    def update(self, url, updates):
        """
        Make a PUT request to save updates
        """
        log.debug("PUT %s" % (url))
        
        put_headers = {"Content-Type": "application/json"}
        put_headers.update(self.__headers)

        response = requests.put(self.full_path(url), data=updates, headers=put_headers)
        
        log.debug("PUT %s status %d" % (url,response.status_code))
        log.debug("OUTPUT: %s" % response.content)
        
        return self._handle_response(url, response)
    
    def create(self, url, data):
        """
        POST request for creating new objects.
        """
        response = requests.post(self.full_path(url), data=data, headers=put_headers)
        return self._handle_response(url, response)
        
    def delete(self, url):
        response = requests.delete(self.full_path(url), data=data, headers=put_headers)
        return self._handle_response(url, response)
    
    def _handle_response(self, url, response):
        """
        Returns parsed JSON or raises an exception appropriately.
        """
        # users see {} in case of 3xx, 202 - should handle?
        result = {}
        if r.status_code in (200, 201, 202):
            result = response.json()
        elif response.status_code == 204:
            raise EmptyResponseWarning("%d %s @ https://%s%s" % (response.status_code, response.reason, self.host, url), 
                                         r.status_code, r.headers, r.content)
        elif response.status_code >= 500:
            raise ServerException("%d %s @ https://%s%s" % (response.status_code, response.reason, self.host, url), 
                                  r.status_code, r.headers, r.content)
        elif response.status_code >= 400:
            log.debug("OUTPUT %s" % response.json())
            raise ClientRequestException("%d %s @ https://%s%s" % (response.status_code, response.reason, self.host, url), 
                                         r.status_code, r.headers, r.content)
        elif response.status_code >= 300:
            raise RedirectionException("%d %s @ https://%s%s" % (response.status_code, response.reason, self.host, url), 
                                         r.status_code, r.headers, r.content)
        return result

    def __repr__(self):
        return "Connection %s" % (self.host)    
