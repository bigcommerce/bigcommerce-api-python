"""
Simple wrapper around requests library, mostly for configuring connection
and usage by resources.
 
The get, post, put, and delete methods of the class could be used directly.
_run_method doc:
    Runs given method (requests.post, .get, .put, .delete)
    with given req_path (the part after /api/v2), and the
    given options keyword args as the query string.
    
    If content is received in response, returns it as
    parsed JSON or raw XML (or other raw data).
"""
 
import requests

from httpexception import *
 
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
    
    # TODO: let user close the session
    # this doesn't need to be instantiated at all to work - change all to classmethod?
 
    @classmethod
    def auth_pair(cls):
        return (cls.user, cls.api_key)
    
    @classmethod
    def full_path(cls, req_path):
        return cls.prtcl_str + cls.host + cls.base_path + req_path
    
    @classmethod
    def _join_options(cls, path, options):
        query_str = '&'.join(['='.join(map(str, item)) for item in options.iteritems()])
        return path + '?' + query_str
    
    @classmethod
    def _run_method(cls, method, req_path, data, **options):
        """
        Runs given method (requests.post, .get, .put, .delete)
        with given req_path (the part after /api/v2), and the
        given options keyword args as the query string.
        
        If content is received in response, returns it as
        parsed JSON or raw XML (or other raw data).
        """
        if options: req_path = cls._join_options(req_path, options)
        r = method(cls.full_path(req_path), auth=cls.auth_pair(), data=data)
        ex = cls._check_response(r)
        if ex:
            ex.message = r.request.method + " request failed:" + ex.message
            raise ex
        else:
            if r.content:
                if r.headers['content-type'] == 'application/json':
                    return r.json()
                else:
                    return r.content

    @classmethod
    def get(cls, req_path, **options):
        return cls._run_method(requests.get, req_path, None, **options)
         
    @classmethod
    def delete(cls, req_path, **options):
        """
        No return value. Exception if not successful.
        """
        return cls._run_method(requests.delete, req_path, None, **options)
 
    @classmethod
    def post(cls, req_path, data, **options):
        return cls._run_method(requests.post, req_path, data, **options)
         
    @classmethod
    def put(cls, req_path, data, **options):
        return cls._run_method(requests.put, req_path, data, **options)

    @classmethod
    def _check_response(cls, r):
        """
        Returns an appropriate HttpException object for 
        status codes other than 2xx, and None otherwise.
        """
        ex = None
        if not r.status_code in (200, 201, 202, 204):
            if r.status_code >= 500:
                ex = ServerException(str(r.content), r.status_code, r.headers, r.content)
            elif r.status_code >= 400:
                ex = ClientRequestException(str(r.content), r.status_code, r.headers, r.content)
            elif r.status_code >= 300:
                ex = RedirectionException(str(r.content), r.status_code, r.headers, r.content)
        return ex