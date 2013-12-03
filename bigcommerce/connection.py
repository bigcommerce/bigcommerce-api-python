"""
This module provides an object-oriented wrapper around the BigCommerce V2 API
for use in Python projects or via the Python shell.

The Connection class should mostly be used to configure the connection details
(host, user, api token, etc). Actual interaction with BigCommerce's REST API should
be done through the appropriate resource classes.
 
If anything isn't well supported, the get, post, put, and delete methods of
the class could be used directly:
    all of the methods take a req_path, which corresponds to the URL substring after /api/v2
        (e.g. /products/5.json)
    all of the methods, except delete, return JSON of the response contents,
        typically the resource made/modified/retrieved
"""
 
import requests

from httpexception import *

# EVERYTHING STILL NEEDS TESTING AAAAAAAAAAAAAAAAAAAAAAAAAAAA
 
API_HOST = 'http://store.mybigcommerce.com'
API_PATH = '/api/v2'
API_USER = 'admin'
API_KEY  = 'yourpasswordhere'
HTTP_PROXY = None
HTTP_PROXY_PORT = 80

class Connection(object):
    """
    Makes connections according to configuration.
    Generally, only host, user, api_key needs to be changed.
    
    Proxies can be defined by doing:
        Connection.proxies = {"http": "http://10.10.1.10:3128",
                              "https": "http://10.10.1.10:1080"}
    
    The four methods corresponding to the http methods return the
    JSON of the response data, or raise an exception if the 
    request failed (see HttpException).
    """
    prtcl_str = "https://"
    host      = API_HOST
    base_path = API_PATH
    user      = API_USER
    api_key   = API_KEY
    proxies   = None
    
    json_headers = {'Content-type':'application/json'}
 
    # requests automatically uses keep-alive
    # TODO: let user close the session
 
    @property
    def auth_pair(self):
        return (self.user, self.api_key)
 
    def full_path(self, req_path):
        return self.prtcl_str + self.host + self.base_path + req_path
 
    def get(self, req_path):
        r = requests.get(self.full_path(req_path), auth=self.auth_pair)
        ex = self._check_response(r)
        if ex:
            ex.message = "GET request failed:" + ex.message
            raise ex
        else:
            return r.json()
         
    def delete(self, req_path):
        """
        No return value. Exception if not successful.
        """
        r = requests.delete(self.full_path(req_path), auth=self.auth_pair)
        ex = self._check_response(r)
        if ex:
            ex.message = "DELETE request failed:" + ex.message
            raise ex
 
    def post(self, req_path, data):
        r = requests.post(self.full_path(req_path), auth=self.auth_pair, headers=self.json_headers, data=data)
        ex = self._check_response(r)
        if ex:
            ex.message = "POST request failed:" + ex.message
            raise ex
        else:
            return r.json()
         
    def put(self, req_path, data):
        r = requests.put(self.full_path(req_path), auth=self.auth_pair, headers=self.json_headers, data=data)
        ex = self._check_response(r)
        if ex:
            ex.message = "PUT request failed:" + ex.message
            raise ex
        else:
            return r.json()

#     exception_classes = {501 : UnsupportedRequest,
#                          503 : ServiceUnavailable,
#                          507 : StorageCapacityError,
#                          509 : BandwidthExceeded,
#                          };
    
    def _check_response(self, r):
        """
        Returns an appropriate HttpException object for 
        status codes other than 2xx, and None otherwise.
        """
        ex = None
#         if exception_classes.has_key(r.status_code):
#             ex = exception_classes[r.status_code](str(r.content))
#         elif not r.status_code in (200, 201, 202, 204):
        # the contents of the responses are very descriptive, so I'll just use those
        if not r.status_code in (200, 201, 202, 204):
            if r.status_code >= 500:
                ex = ServerException(str(r.content), r.headers, r.content)
            elif r.status_code >= 400:
                ex = ClientRequestException(str(r.content), r.headers, r.content)
            elif r.status_code >= 300:
                ex = RedirectionException(str(r.content), r.headers, r.content)
        return ex
    
    
"""
STUFF THAT NEEDS IMPLEMENTIN or something??
    def verify_ssl=(verify)
      @connection.verify_ssl = verify
    end

    def ca_file=(path)
      @connection.ca_file = path
    end

    def to_rfc2822(datetime)
      datetime.strftime("%a, %d %b %Y %H:%M:%S %z")
    end

*    def get_time 
      @connection.get '/time'
    end

* currently not supporting options (query strings?)

- counts by len()

    def get_countries_states(options={})
      @connection.get("/countries/states", options)
    end

    def get_countries_state(id, options={})
      @connection.get("/countries/#{id}/states", {})
    end

    def get_customer_addresses(id, options = {})
      @connection.get("/customers/#{id}/addresses", options)
    end

    def get_customer_address(customer_id, address_id)
      @connection.get("/customers/#{customer_id}/addresses/#{address_id}",{})
    end

    def get_options_values(options={})
       @connection.get("/options/values", options)
    end

    def get_options_value(id)
      @connection.get("/options/#{id}/values",{})
    end

    def create_options_values(options_id, options={})
      @connection.post("/options/#{options_id}/values", options)
    end

    def update_options_value(options_id, values_id, options={})
      @connection.put("/options/#{options_id}/values/#{values_id}", options)
    end   

    def get_optionsets_options(options={})
       @connection.get("/optionsets/options", options)
    end

    def get_optionset_options(id)
      @connection.get("/optionsets/#{id}/options", {})
    end

    def get_optionsets_option(id)
      @connection.get("/optionsets/options/#{id}", {})
    end

    def create_optionset_option(id, options={})
      @connection.post("/optionsets/#{id}/options", options)
    end

    def update_optionset_option(optionset_id, option_id, options={})
      @connection.put("/optionsets/#{optionset_id}/options/#{option_id}", options)
    end

    def get_orders_by_date(date, options={})
      if date.is_a?(String)
        date = DateTime.parse(date)
      end
      @connection.get('/orders', options.merge!(:min_date_created => to_rfc2822(date)))
    end

    def get_orders_modified_since(date)
      @connection.get('/orders', {}, {'If-Modified-Since' => to_rfc2822(date)})
    end

    def get_orders_coupons(id)
      @connection.get("/orders/#{id}/coupons", {})
    end

    def get_orders_coupon(order_id,coupon_id)
      @connection.get("/orders/#{order_id}/coupons/#{coupon_id}", {})
    end

    def get_orders_products(id)
      @connection.get("/orders/#{id}/products", {})
    end

    def get_orders_product(order_id,product_id)
      @connection.get("/orders/#{order_id}/products/#{product_id}", {})
    end

    def get_orders_shipments(id)
      @connection.get("/orders/#{id}/shipments", {})
    end

    def create_orders_shipments(id, options={})
      @connection.post("/orders/#{id}/shipments", options)
    end

    def get_orders_shipment(order_id,shipment_id)
      @connection.get("/orders/#{order_id}/shipments/#{shipment_id}", {})
    end

    def update_orders_shipment(order_id,shipment_id,options={})
      @connection.put("/orders/#{order_id}/shipments/#{shipment_id}", options)
    end

    def get_orders_shippingaddresses(id)
      @connection.get("/orders/#{id}/shippingaddresses", {})
    end

    def get_orders_shippingaddress(order_id,shippingaddress_id)
      @connection.get("/orders/#{order_id}/shippingaddresses/#{shippingaddress_id}", {})
    end

    def get_orderstatuses(options={})
      @connection.get("/orderstatuses", options)
    end

    def get_orderstatus(id)
      @connection.get("/orderstatuses/#{id}", {})
    end

    def update_products(id, options={})
      @connection.put("/products/#{id}", options)
    end

    def get_products_discountrules(options={})
      @connection.get("/products/discountrules", options)
    end

    def get_product_discountrules(product_id, options={})
      @connection.get("/products/#{product_id}/discountrules", options)
    end

    def get_products_discountrule(product_id, discountrule_id)
      @connection.get("/products/#{product_id}/discountrules/#{discountrule_id}", {})
    end

    def get_products_configurablefields(options={})
      @connection.get("/products/configurablefields", options)
    end

    def get_product_configurablefields(product_id, options={})
      @connection.get("/products/#{product_id}/configurablefields", options)
    end

    def get_products_configurablefield(product_id, configurable_field_id)
      @connection.get("/products/#{product_id}/configurablefields/#{configurable_field_id}", {})
    end

    def get_products_customfields(options={})
      @connection.get("/products/customfields", options)
    end

    def get_product_customfields(product_id, options={})
      @connection.get("/products/#{product_id}/customfields", options)
    end

    def get_products_customfield(product_id, custom_field_id)
      @connection.get("/products/#{product_id}/customfields/#{custom_field_id}", {})
    end

    def get_product_images(product_id, options={})
      @connection.get("/products/#{product_id}/images", options)
    end

    def create_product_images(product_id, options={})
      @connection.post("/products/#{product_id}/images", options)
    end

    def get_products_images(options={})
      @connection.get("/products/images", options)
    end

    def create_products_images(options={})
      @connection.post("/products/images", options)
    end

    def get_products_image(product_id, image_id)
      @connection.get("/products/#{product_id}/images/#{image_id}", {})
    end

    def update_products_image(product_id,image_id,options={})
      @connection.put("/products/#{product_id}/images/#{image_id}", options)
    end

    def get_products_customfields(options={})
      @connection.get("/products/options", options)
    end

    def get_product_options(product_id, options={})
      @connection.get("/products/#{product_id}/options", options)
    end

    def get_products_option(product_id,option_id)
      @connection.get("/products/#{product_id}/options/#{option_id}", {})
    end

    def get_products_rules(options={})
      @connection.get("/products/rules", options)
    end

    def get_product_rules(product_id, options={})
      @connection.get("/products/#{product_id}/rules", options)
    end

    def create_products_rules(options={})
      @connection.post("/products/rules", options)
    end

    def get_products_rule(product_id,rule_id)
      @connection.get("/products/#{product_id}/rules/#{rule_id}", {})
    end

    def update_products_rule(product_id, rule_id, options={})
      @connection.put("/products/#{product_id}/rules/#{rule_id}", options)
    end

    def get_products_skus(options={})
      @connection.get("/products/skus", options)
    end

    def get_product_skus(product_id, options={})
      @connection.get("/products/#{product_id}/skus", options)
    end

    def create_products_skus(options={})
      @connection.post("/products/skus", options)
    end

    def get_products_sku(product_id, sku_id)
      @connection.get("/products/#{product_id}/skus/#{sku_id}", {})
    end

    def update_products_sku(product_id, sku_id, options={})
      @connection.put("/products/#{product_id}/skus/#{sku_id}", options)
    end

    def get_products_videos(options={})
      @connection.get("/products/videos", options)
    end

    def get_product_videos(product_id, options={})
      @connection.get("/products/#{product_id}/videos", options)
    end

    def get_products_video(product_id, video_id)
      @connection.get("/products/#{product_id}/videos/#{video_id}", {})
    end

    private

    def get_count(result)
      result["count"]
    end

    def get_resource(result)
      result
    end

    def get_collection(result)
      result
    end

  end
end
"""