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

API_HOST = 'http://store.mybigcommerce.com'
API_PATH = '/api/v2'
API_USER = 'admin'
API_KEY  = 'yourpasswordhere'

"""
Contains exceptions for the user's convenience
in responding to random crap happening.
"""

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

class Connection(object):
    """
    Makes connections according to configuration.
    Generally, only host, user, api_key needs to be changed.
    
    Proxies can be defined by doing:
        Connection.proxies = {"http": "http://10.10.1.10:3128",
                              "https": "http://10.10.1.10:1080"}
    Custom headers can also be defined (requests tends to handle everything):
        Connection.headers = {'content-type' : 'application/xml'}
    Set back to None to disable.
    
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
    headers   = None
    
    # instead of using requests.get methods, can create and hold session instance 
    # (as class variable) on demand and use that (which is what requests does anyway)
    # and let user close it if they wish
    # -> would user ever really want to manually close sessions? does requests ever do that automatically?
    # also see (for session objects):
    #     Note that connections are only released back to the pool for reuse once all body data has been read; 
    #     be sure to either set stream to False or read the content property of the Response object.
 
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
        #TODO: in which cases would users not want parsed JSON returned?
        if options: req_path = cls._join_options(req_path, options)
        r = method(cls.full_path(req_path), auth=cls.auth_pair(), data=data, 
                   proxies=cls.proxies,
                   headers=cls.headers)
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

    #TODO: maybe CRUD naming would be better... not important?

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