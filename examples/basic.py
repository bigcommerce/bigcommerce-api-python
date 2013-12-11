STORE_HOST = "www.YOURHOST.com"
STORE_TOKEN = "YOUR_TOKEN"
STORE_USERID = "userid"
from settings import *
import sys
import logging
from pprint import pprint
from Bigcommerce.api import ApiClient

logging.basicConfig(level=logging.DEBUG, 
                    stream=sys.stdout,
                    format='%(asctime)s %(levelname)-8s[%(name)s] %(message)s',
                    datefmt='%m/%d %H:%M:%S')
log = logging.getLogger("main")

if __name__ == "__main__":
    log.debug("HOST %s, USER: %s" % (STORE_HOST, STORE_USERID))
    api = ApiClient(STORE_HOST, STORE_TOKEN, STORE_USERID)
    
    filters = api.Products.filters()
    
    
    # List 10 products starting at offset 10
    for product in api.Products.enumerate(start=10, limit=10, query=filters):
        print product.id, product.sku, product.name, product.price
        pass
    
    
    order = api.Orders.get(101)
    print "Order", order.id, order.date_created
    for product in order.products:
        print product.quantity, product.name
        
    