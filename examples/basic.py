STORE_HOST = "www.YOURHOST.com"
STORE_TOKEN = "YOUR_TOKEN"
STORE_USERID = "userid"
from settings import *
import sys
import logging
from pprint import pprint
from bigcommerce.api import bigCommerce

logging.basicConfig(level=logging.DEBUG, 
                    stream=sys.stdout,
                    format='%(asctime)s %(levelname)-8s[%(name)s] %(message)s',
                    datefmt='%m/%d %H:%M:%S')


if __name__ == "__main__":
    api = bigCommerce(STORE_HOST, STORE_TOKEN, STORE_USERID)
    
    filters = api.Products.filters()
    filters.min_id.set(73873)
    
    # List 10 products starting at offset 10
    for product in api.Products.enumerate(start=10, limit=10, query=filters):
        print product.id, product.sku, product.name, product.price
        pass
    
    