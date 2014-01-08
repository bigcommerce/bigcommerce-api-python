"""
Connection Module

Handles put and get operations to the Bigcommerce REST API
"""

import urllib, json  # only used for urlencode querystr
import logging
from pprint import pformat  # only used once for logging, in __load_urls

import requests

from resources.mapping import Mapping
from httpexception import *

log = logging.getLogger("Bigcommerce.com")


class Connection(object):
    """
    Connection class manages the connection to the Bigcommerce REST API.
    """
    
    def __init__(self, host, auth, api_path='/api/v2/{}', map_wrap=True):
        """
        On creation, an initial call is made to load the mappings of resources to URLs.
        
        If map_wrap is set, results returned will be Mapping objects, allowing for dot access
        (as well as being standard dictionaries).
        """
        self.host = host
        self.api_path = api_path
        
        self.timeout = 7.0  # need to catch timeout?
        
        log.info("API Host: %s/%s" % (self.host, self.api_path))

        self._map_wrap = map_wrap

        # set up the session
        self._session = requests.Session()
        self._session.auth = auth
        self._session.headers = {"Accept": "application/json"}

        self.__resource_meta = self.get()  # retrieve metadata about urls and resources
        log.debug(pformat(self.__resource_meta))
        
        self._last_response = None  # for debugging
        
    def meta_data(self):
        """
        Return a JSON string representation of resource-to-url mappings 
        """
        return json.dumps(self.__resource_meta)
        
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
        return "https://" + self.host + self.api_path.format(url)
    
    def _run_method(self, method, url, data=None, query={}, headers={}):
        # make full path if not given
        if url and url[:4] != "http":
            if url[0] == '/':  # can call with /resource if you want
                url = url[1:]
            url = self.full_path(url)
        elif not url:  # blank path
            url = self.full_path(url)

        qs = urllib.urlencode(query)
        if qs: qs = "?" + qs
        url += qs

        # mess with content
        if data:
            if not headers:  # assume JSON
                data = json.dumps(data)
                headers = {'Content-Type': 'application/json'}
            if headers and not 'Content-Type' in headers:
                data = json.dumps(data)
                headers['Content-Type'] = 'application/json'
        log.debug("%s %s" % (method, url))
        # make and send the request
        return self._session.request(method, url, data=data, timeout=self.timeout, headers=headers)

    def get(self, url="", **query):
        """
        Perform the GET request and return the parsed results
        """
        response = self._run_method('GET', url, query=query)
        return self._handle_response(url, response)
        
    def update(self, url, updates):
        """
        Same as put
        """
        response = self._run_method('PUT', url, data=updates)
        log.debug("OUTPUT: %s" % response.content)
        return self._handle_response(url, response)

    def put(self, url, updates):
        """
        Make a PUT request to save updates.
        updates should be a dictionary.
        """
        response = self._run_method('PUT', url, data=updates)
        log.debug("OUTPUT: %s" % response.content)
        return self._handle_response(url, response)

    def create(self, url, data):
        """
        Same as post
        """
        response = self._run_method('POST', url, data=data)
        return self._handle_response(url, response)

    def post(self, url, data, headers={}):
        """
        POST request for creating new objects.
        data should be a dictionary.
        """
        response = self._run_method('POST', url, data=data, headers=headers)
        return self._handle_response(url, response)
        
    def delete(self, url, id_=None):  # note that id_ can't be 0 - problem?
        if id_:
            if url[-1] != '/': url += '/'
            url += str(id_)
        response = self._run_method('DELETE', url)
        return self._handle_response(url, response, suppress_empty=True)
    
    def _handle_response(self, url, res, suppress_empty=False):
        """
        Returns parsed JSON or raises an exception appropriately.
        """
        self._last_response = res
        result = {}
        if res.status_code in (200, 201, 202):
            try:
                result = res.json()
            except Exception as e:  # json might be invalid, or store might be down
                e.message += " (_handle_response failed to decode JSON: " + str(res.content) + ")"
                raise  # TODO better exception
            if self._map_wrap:
                if isinstance(result, list):
                    return map(Mapping, result)
                else:
                    return Mapping(result)
            else: return result
        elif res.status_code == 204 and not suppress_empty:
            raise EmptyResponseWarning("%d %s @ %s: %s" % (res.status_code, res.reason, url, res.content), res)
        elif res.status_code >= 500:
            raise ServerException("%d %s @ %s: %s" % (res.status_code, res.reason, url, res.content), res)
        elif res.status_code >= 400:
            raise ClientRequestException("%d %s @ %s: %s" % (res.status_code, res.reason, url, res.content), res)
        elif res.status_code >= 300:
            raise RedirectionException("%d %s @ %s: %s" % (res.status_code, res.reason, url, res.content), res)
        return result

    def __repr__(self):
        return "%s %s%s" % (self.__class__.__name__, self.host, self.api_path)
