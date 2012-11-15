from settings import *
import sys
import logging
from pprint import pprint
from bigcommerce.api import bigCommerce

logging.basicConfig(level=logging.DEBUG, 
                    stream=sys.stdout,
                    format='%(asctime)s %(levelname)-8s[%(name)s] %(message)s',
                    datefmt='%m/%d %H:%M:%S')
log = logging.getLogger("main")

if __name__ == "__main__":
    log.debug("HOST %s, USER: %s" % (STORE_HOST, STORE_USERID))
    api = bigCommerce(STORE_HOST, STORE_TOKEN, STORE_USERID)
    
    product = api.Products.get(14)
    
    print product.images[1].is_thumbnail
    
    product.images[1].is_thumbnail = True
    product.images[1].save()
    print product.images[1].is_thumbnail