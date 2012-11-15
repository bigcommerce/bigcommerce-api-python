import os
import sys
import base64
import logging

from bigcommerce.api.lib.connection import Connection
from resources import ResourceAccessor

log = logging.getLogger("bc_aaapi")


class bigCommerce(object):
    BASE_URL = '/api/v2'
    
    def __init__(self, host, token, user_id):
        auth = base64.b64encode("%s:%s" % (user_id, token))
        self._connection = Connection(host, self.BASE_URL, auth)
        
        
    def connection(self):
        pass
    
    def show_urls(self):
        self._connection.dump_meta()
        
    def __getattr__(self, attrname):
        try:
            return ResourceAccessor(attrname, self._connection)
        except:
            raise AttributeError
        raise AttributeError
            