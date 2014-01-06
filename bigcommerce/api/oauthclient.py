import logging

from bigcommerce.api.oauthconnection import OAuthConnection
from bigcommerce.api.resources.resource import ResourceAccessor

log = logging.getLogger("Bigcommerce.api")


class OAuthClient(object):
    BASE_URL = '/api/v2'
    
    def __init__(self, client_id, store_hash, access_token=None,
                 host='api.bigcommerceapp.com', api_path='/stores/{}/v2/{}'):
        self.connection = OAuthConnection(client_id, store_hash,
                                          host=host,
                                          api_path=api_path,
                                          access_token=access_token,
                                          map_wrap=False)
        
    def get_url_registry(self): # this is used precisely once - in the enum_classes test
        return self.connection.meta_data()
        
    def __getattr__(self, attrname):
        try:
            return ResourceAccessor(attrname, self.connection)
        except Exception as e:  # TODO: what errors would this even raise?
            raise AttributeError(str(e))