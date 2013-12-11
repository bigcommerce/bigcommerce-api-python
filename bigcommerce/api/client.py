import os
import sys
import base64
import logging

from bigcommerce.api.connection import Connection
from bigcommerce.api.resource import ResourceAccessor

log = logging.getLogger("Bigcommerce.api")

class Client(object):
    BASE_URL = '/api/v2'
    
    def __init__(self, host, token, user_id):
        auth = base64.b64encode("%s:%s" % (user_id, token)) # not necessary - requests does this
        self._connection = Connection(host, self.BASE_URL, auth)
        
    def connection(self): # what's this for?
        pass
    
    def get_url_registry(self): # this is used precisely once - in the enum_classes test
        return self._connection.meta_data()
        
    def __getattr__(self, attrname):
        try:
            return ResourceAccessor(attrname, self._connection)
        except:
            raise AttributeError
        raise AttributeError