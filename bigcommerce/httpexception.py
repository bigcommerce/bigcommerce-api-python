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