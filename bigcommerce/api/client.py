import os
import sys
import logging

from bigcommerce.api.connection import Connection
from bigcommerce.api.resources.resource import ResourceAccessor

log = logging.getLogger("Bigcommerce.api")

class Client(object):
    BASE_URL = '/api/v2'
    
    def __init__(self, host, token, user_id):
        self.connection = Connection(host, (user_id, token), self.BASE_URL, map_wrap=False)
        
    def get_url_registry(self): # this is used precisely once - in the enum_classes test
        return self.connection.meta_data()
        
    def __getattr__(self, attrname):
        try:
            return ResourceAccessor(attrname, self.connection)
        except Exception as e: # TODO: what errors would this even raise?
            raise AttributeError(str(e))
        raise AttributeError