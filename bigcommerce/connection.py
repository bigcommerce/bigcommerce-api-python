"""
This module provides an object-oriented wrapper around the BigCommerce V2 API
for use in Python projects or via the Python shell.

The Connection class should mostly be used to configure the connection details
(host, user, api token, etc). Actual interaction with BigCommerce's REST API should
be done through the appropriate resource classes.
 
If needed for some reason, the get, post, put, and delete methods of
the class could be used directly:
    all of the methods take a req_path, which corresponds to the URL substring after /api/v2
        (e.g. /products/5.json)
    all of the methods, except delete, return parsed JSON of the response contents,
        typically containing the fields of the resource made/modified/retrieved.
        The parsed JSON can be used to construct Resource objects.
"""
 
import requests

from httpexception import *

# EVERYTHING STILL NEEDS TESTING AAAAAAAAAAAAAAAAAAAAAAAAAAAA
 
API_HOST = 'http://store.mybigcommerce.com'
API_PATH = '/api/v2'
API_USER = 'admin'
API_KEY  = 'yourpasswordhere'
HTTP_PROXY = None
HTTP_PROXY_PORT = 80

class Connection(object):
    """
    Makes connections according to configuration.
    Generally, only host, user, api_key needs to be changed.
    
    Proxies can be defined by doing:
        Connection.proxies = {"http": "http://10.10.1.10:3128",
                              "https": "http://10.10.1.10:1080"}
    
    The four methods corresponding to the http methods return the
    JSON of the response data (or None if no data received), or raise 
    an exception if the request failed (see HttpException).
    """
    prtcl_str = "https://"
    host      = API_HOST
    base_path = API_PATH
    user      = API_USER
    api_key   = API_KEY
    proxies   = None
    
    json_headers = {'Content-type':'application/json'}
 
    # requests automatically uses keep-alive
    # TODO: let user close the session
 
    @property
    def auth_pair(self):
        return (self.user, self.api_key)
 
    def full_path(self, req_path):
        return self.prtcl_str + self.host + self.base_path + req_path

    def _join_options(self, path, options):
        query_str = '&'.join(['='.join(map(str, item)) for item in options.iteritems()])
        return path + '?' + query_str

    def get(self, req_path, options=None):
        if options: req_path = self._join_options(req_path, options)
        r = requests.get(self.full_path(req_path), auth=self.auth_pair)
        ex = self._check_response(r)
        if ex:
            ex.message = "GET request failed:" + ex.message
            raise ex
        else:
            return r.json() if r.content else None
         
    def delete(self, req_path, options=None):
        """
        No return value. Exception if not successful.
        """
        if options: req_path = self._join_options(req_path, options)
        r = requests.delete(self.full_path(req_path), auth=self.auth_pair)
        ex = self._check_response(r)
        if ex:
            ex.message = "DELETE request failed:" + ex.message
            raise ex
 
    def post(self, req_path, data, options=None):
        if options: req_path = self._join_options(req_path, options)
        r = requests.post(self.full_path(req_path), auth=self.auth_pair, headers=self.json_headers, data=data)
        ex = self._check_response(r)
        if ex:
            ex.message = "POST request failed:" + ex.message
            raise ex
        else:
            return r.json() if r.content else None
         
    def put(self, req_path, data, options=None):
        if options: req_path = self._join_options(req_path, options)
        r = requests.put(self.full_path(req_path), auth=self.auth_pair, headers=self.json_headers, data=data)
        ex = self._check_response(r)
        if ex:
            ex.message = "PUT request failed:" + ex.message
            raise ex
        else:
            return r.json() if r.content else None

#     exception_classes = {501 : UnsupportedRequest,
#                          503 : ServiceUnavailable,
#                          507 : StorageCapacityError,
#                          509 : BandwidthExceeded,
#                          };
    
    def _check_response(self, r):
        """
        Returns an appropriate HttpException object for 
        status codes other than 2xx, and None otherwise.
        """
        ex = None
#         if exception_classes.has_key(r.status_code):
#             ex = exception_classes[r.status_code](str(r.content))
#         elif not r.status_code in (200, 201, 202, 204):
        # the contents of the responses are very descriptive, so I'll just use those
        if not r.status_code in (200, 201, 202, 204):
            if r.status_code >= 500:
                ex = ServerException(str(r.content), r.headers, r.content)
            elif r.status_code >= 400:
                ex = ClientRequestException(str(r.content), r.headers, r.content)
            elif r.status_code >= 300:
                ex = RedirectionException(str(r.content), r.headers, r.content)
        return ex