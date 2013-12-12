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
    
    def __init__(self, host, base_url, auth):
        """
        On creation, an initial call is made to load the mappings of resources to URLs
        """
        self.host = host
        self.base_url = base_url
        self.auth = auth
        
        log.info("API Host: %s/%s" % (self.host, self.base_url))
        log.debug("Accepting json") #, auth: Basic %s" % self.auth)
        
        # TODO: would like to let people use Connection directly and grab XML data if they want
        # maybe just an xml_mode flag would be enough
        self.__headers = {"Accept" : "application/json"}

        self.__resource_meta = {}
        self.__load_urls()
        
        
    def meta_data(self):
        """
        Return a JSON string representation of resource-to-url mappings 
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
        return self.__resource_meta.get(resource_name, {}).get("url", None)
    
    def get_resource_url(self, resource_name):
        """
        Lookup the "resource" for the resource name from the internally stored resource mappings
        """
        return self.__resource_meta.get(resource_name, {}).get("resource", None)

    def full_path(self, url):
        return "https://" + self.host + self.base_url + url
    
    # could use a session to save the auth and __headers - keeping as is for now
    
    def get(self, url="", query={}):
        """
        Perform the GET request and return the parsed results
        """
        qs = urllib.urlencode(query)
        if qs:
            qs = "?%s" % qs
        log.debug("GET %s%s" % (url, qs))
        url = self.full_path("%s%s" % (url, qs))
        
        response = requests.get(url, auth=self.auth, headers=self.__headers)
        
        log.debug("GET %s status %d" % (url,response.status_code))
        
        return self._handle_response(url, response)
        
    def update(self, url, updates):
        """
        Make a PUT request to save updates
        """
        log.debug("PUT %s" % (url))
        url = self.full_path(url)
        response = requests.put(url, auth=self.auth, data=updates, headers=self.__headers)
        
        log.debug("PUT %s status %d" % (url,response.status_code))
        log.debug("OUTPUT: %s" % response.content)
        return self._handle_response(url, response)
    
    def create(self, url, data):
        """
        POST request for creating new objects.
        """
        url = self.full_path(url)
        response = requests.post(url, auth=self.auth, data=data, headers=self.__headers)
        return self._handle_response(url, response)
        
    def delete(self, url):
        url = self.full_path(url)
        response = requests.delete(url, auth=self.auth, headers=self.__headers)
        return self._handle_response(url, response, suppress_empty=True)
    
    def _handle_response(self, url, res, suppress_empty=False):
        """
        Returns parsed JSON or raises an exception appropriately.
        """
        result = {}
        if res.status_code in (200, 201, 202):
            result = res.json()
        elif res.status_code == 204 and not suppress_empty:
            raise EmptyResponseWarning("%d %s @ %s" % (res.status_code, res.reason, url), 
                                         res.status_code, res.headers, res.content)
        elif res.status_code >= 500:
            raise ServerException("%d %s @ %s" % (res.status_code, res.reason, url), 
                                  res.status_code, res.headers, res.content)
        elif res.status_code >= 400:
            log.debug("OUTPUT %s" % res.json())
            raise ClientRequestException("%d %s @ %s" % (res.status_code, res.reason, url), 
                                         res.status_code, res.headers, res.content)
        elif res.status_code >= 300:
            raise RedirectionException("%d %s @ %s" % (res.status_code, res.reason, url), 
                                         res.status_code, res.headers, res.content)
        return result

    def __repr__(self):
        return "Connection %s" % (self.host)    
