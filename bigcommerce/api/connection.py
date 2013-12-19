"""
Connection Module

Handles put and get operations to the Bigcommerce REST API
"""

import urllib # only used for urlencode querystr
import logging
import simplejson
from pprint import pformat # only used once, in __load_urls

import requests

log = logging.getLogger("Bigcommerce.com")

class HttpException(Exception):
    """
    Class for representing http errors. Contains the response.
    """
    def __init__(self, msg, res):
        super(Exception, self).__init__(msg)
        self.response = res
        
    @property
    def status_code(self):
        return self.response.status_code
    @property
    def headers(self):
        return self.response.headers
    @property
    def content(self):
        return self.response.content
  
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
        
        self.timeout = 7.0 # need to catch timeout?
        
        log.info("API Host: %s/%s" % (self.host, self.base_url))
        
        # set up the session
        self._session = requests.Session()
        self._session.auth = auth
        self._session.headers = {"Accept" : "application/json"}

        self.__resource_meta = self.get() # retrieve metadata about urls and resources
        log.debug(pformat(self.__resource_meta))
        
        
    def meta_data(self):
        """
        Return a JSON string representation of resource-to-url mappings 
        """
        return simplejson.dumps(self.__resource_meta)    
        
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
    
    # could use a session to save the auth and _headers - keeping as is for now
    
    def _run_method(self, method, url, data=None, query={}):
        # make full path
        qs = urllib.urlencode(query)
        if qs: qs = "?" + qs
        url = self.full_path("%s%s" % (url, qs))
        # mess with content
        if data:
            data = simplejson.dumps(data)
            headers = {'Content-Type' : 'application/json'}
        else: headers = None
        log.debug("%s %s%s" % (method, url, qs))
        # make and send the request
        return self._session.request(method, url, data=data, timeout=self.timeout, headers=headers)
    
    def get(self, url="", query={}):
        """
        Perform the GET request and return the parsed results
        """
        response = self._run_method('GET', url, query=query)
        return self._handle_response(url, response)
        
    def update(self, url, updates):
        """
        Make a PUT request to save updates
        """
        response = self._run_method('PUT', url, data=updates)
        log.debug("OUTPUT: %s" % response.content)
        return self._handle_response(url, response)
    
    def create(self, url, data):
        """
        POST request for creating new objects.
        """
        response = self._run_method('POST', url, data=data)
        return self._handle_response(url, response)
        
    def delete(self, url):
        response = self._run_method('DELETE', url)
        return self._handle_response(url, response, suppress_empty=True)
    
    def _handle_response(self, url, res, suppress_empty=False):
        """
        Returns parsed JSON or raises an exception appropriately.
        """
        log.debug("STATUS CODE: %s" % res.status_code)
        result = {}
        if res.status_code in (200, 201, 202):
            result = res.json()
        elif res.status_code == 204 and not suppress_empty:
            raise EmptyResponseWarning("%d %s @ %s: %s" % (res.status_code, res.reason, url, res.content), 
                                         res)
        elif res.status_code >= 500:
            raise ServerException("%d %s @ %s: %s" % (res.status_code, res.reason, url, res.content), 
                                  res)
        elif res.status_code >= 400:
            raise ClientRequestException("%d %s @ %s: %s" % (res.status_code, res.reason, url, res.content), 
                                         res)
        elif res.status_code >= 300:
            raise RedirectionException("%d %s @ %s: %s" % (res.status_code, res.reason, url, res.content), 
                                         res)
        return result

    def __repr__(self):
        return "Connection %s%s" % (self.host, self.base_url)    
