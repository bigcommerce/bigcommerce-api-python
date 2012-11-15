import sys
import math
import base64
import logging
import settings
import simplejson
from pprint import pprint

import urllib
from urlparse import urlparse
from httplib import HTTPSConnection, HTTPException

 
log = logging.getLogger("bc_api")

class EmptyResponseWarning(HTTPException):
    pass


class Connection():
    
    def __init__(self, host, base_url, auth):
        """
        Constructor
        """
        self.host = host
        self.base_url = base_url
        self.auth = auth
        log.info("API Host: %s" % (self.base_url))
        log.debug("Accepting json, auth: Basic %s" % self.auth)
        self.__headers = {"Authorization": "Basic %s" % self.auth,
                        "Accept": "application/json"}
        
        self.__resource_meta = {}
        self.__connection = HTTPSConnection(self.host)
        self.__load_urls()
        
        
        
    def __load_urls(self):
        """
        Hit the base url and get the urls and resources from 
        the server
        """
        self.__resource_meta = self.get()
        
    
    def get(self, url="", query={}):
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
        
        log.debug("GET %s status %d" % (url,response.status))
        result = {}
        
        if response.status == 200:
            result = simplejson.loads(data)
            #log.debug("OUTPUT %s" % result)
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
        return self.__resource_meta.get(resource_name,{}).get("url", None)
    
    def get_resource_url(self, resource_name):
        return self.__resource_meta.get(resource_name,{}).get("resource", None)
        
    def update(self, url, updates):
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
            #log.debug("OUTPUT %s" % result)
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
        return "Connection %s auth %s" % (self.host, self.auth)
    
    


    