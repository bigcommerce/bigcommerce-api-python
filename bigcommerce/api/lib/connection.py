"""
Connection Module

Handles put and get operations to the Bigcommerce REST API
"""
import sys
import urllib
import logging
import simplejson
from urlparse import urlparse
from pprint import pprint, pformat
from httplib import HTTPSConnection, HTTPException

 
log = logging.getLogger("BigCommerce.con")

class EmptyResponseWarning(HTTPException):
    pass


class Connection():
    """
    Connection class manages the connection to the Bigcommerce REST API.
    """
    
    def __init__(self, host, base_url, auth):
        """
        Constructor
        
        On creation, an initial call is made to load the mappings of resources to URLS
        """
        self.host = host
        self.base_url = base_url
        self.auth = auth
        
        log.info("API Host: %s/%s" % (self.host, self.base_url))
        log.debug("Accepting json, auth: Basic %s" % self.auth)
        self.__headers = {"Authorization": "Basic %s" % self.auth,
                        "Accept": "application/json"}
        
        self.__resource_meta = {}
        self.__connection = HTTPSConnection(self.host)
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
        
    
    def get(self, url="", query={}):
        """
        Perform the GET request and return the parsed results
        """
        qs = urllib.urlencode(query)
        if qs:
            qs = "?%s" % qs
            
        url = "%s%s%s" % (self.base_url, url, qs)
        log.debug("GET %s" % (url))
        
        self.__connection.connect()
        request = self.__connection.request("GET", url, None, self.__headers)
        response = self.__connection.getresponse()
        data = response.read()
        self.__connection.close()
        log.debug(pformat(response.getheaders()))
        log.debug("GET %s status %d" % (url,response.status))
        result = {}
        
        # Check the return status
        if response.status == 200:
            result = simplejson.loads(data)
            log.debug("%s" % pformat(result))
        elif response.status == 204:
            raise EmptyResponseWarning("%d %s @ https://%s%s" % (response.status, response.reason, self.host, url))
        
        elif response.status == 404:
            log.debug("%s returned 404 status" % url)
            raise HTTPException("%d %s @ https://%s%s" % (response.status, response.reason, self.host, url))
        
        elif response.status >= 400:
            _result = simplejson.loads(data)
            log.debug("OUTPUT %s" % _result)
            raise HTTPException("%d %s @ https://%s%s" % (response.status, response.reason, self.host, url))
        
        return result
    
    
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
        
        
    def update(self, url, updates):
        """
        Make a PUT request to save updates
        """
        url = "%s%s" % (self.base_url, url)
        log.debug("PUT %s" % (url))
        self.__connection.connect()
        
        put_headers = {"Content-Type": "application/json"}
        put_headers.update(self.__headers)
        request = self.__connection.request("PUT", url, simplejson.dumps(updates), put_headers)
        response = self.__connection.getresponse()
        data = response.read()
        self.__connection.close()
        
        log.debug("PUT %s status %d" % (url,response.status))
        log.debug("OUTPUT: %s" % data)
        
        result = {}
        if response.status == 200:
            result = simplejson.loads(data)
        
        elif response.status == 204:
            raise EmptyResponseWarning("%d %s @ https://%s%s" % (response.status, response.reason, self.host, url))
        
        elif response.status == 404:
            log.debug("%s returned 404 status" % url)
            raise HTTPException("%d %s @ https://%s%s" % (response.status, response.reason, self.host, url))
        
        elif response.status >= 400:
            _result = simplejson.loads(data)
            log.debug("OUTPUT %s" % _result)
            raise HTTPException("%d %s @ https://%s%s" % (response.status, response.reason, self.host, url))
        
        return result
    
    
    def __repr__(self):
        return "Connection %s" % (self.host)
    
    


    