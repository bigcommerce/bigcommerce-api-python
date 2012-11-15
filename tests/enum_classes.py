from settings import *
import sys
import logging
from pprint import pprint, pformat
from Bigcommerce.api import ApiClient

logging.basicConfig(level=logging.INFO, 
                    stream=sys.stdout,
                    format='%(asctime)s %(levelname)-8s[%(name)s] %(message)s',
                    datefmt='%m/%d %H:%M:%S')

log = logging.getLogger("test")
elog = logging.getLogger("ENUM")
slog = logging.getLogger("SUBRES")

def test_subresource(resource):
    slog.info("Resource: %s" % resource.name)
    
    for res in resource.enumerate(limit=1):
        slog.info("Using %s" % res)
        
        for prop, meta in resource.get_subresources().items():
            slog.info("\tSubResource %s [single:%s]" % (prop, meta.get("single", False)))
            try:
                if meta.get("single", False):
                    slog.info("\t\t%s" %  getattr(res, prop))
                else:
                    for r in getattr(res, prop):
                        slog.info("\t\t%s" %  r)
            except AttributeError as e:
                slog.error("\t\tError enumerating %s %s" % (prop, e))
            except:
                slog.error("\t\tError enumerating %s" % (prop))
    log.info("%s\n" % ("=" * 20))


def test_resource_enum(resource, details=True):
    """
    Make sure the count matches the number of items enumerated
    """
    elog.info("Resource: %s" % resource.name)
    
    expected = 0
    try:
        expected = resource.get_count()
        elog.info("\t%d instances" % expected)
    except:
        elog.error("\tget_count Failed")
    
    count = 0
    for r in resource.enumerate():
        if details:
            elog.info("\t\t%s" % r)
        count += 1
    
    if count == expected:
        elog.info("\tExpected number of items enumerated")
    else:
        elog.error("\tEnumerated %d" % count)
    
    log.info("%s\n" % ("=" * 20))   
    

                
def test_resource(resource):
    test_resource_enum(resource)
    test_subresource(resource)       

        

if __name__ == "__main__":
    log.debug("HOST %s, USER: %s" % (STORE_HOST, STORE_USERID))
    api = ApiClient(STORE_HOST, STORE_TOKEN, STORE_USERID)
    api.show_urls()
    
    
    test_resource(api.Brands)
    test_resource(api.Categories)
    test_resource(api.Customers)
    test_resource(api.Options)
    test_resource(api.OptionSets)
    test_resource(api.Orders)
    test_resource(api.Products)
    test_resource(api.OrderStatuses)
    
    
    
    
    