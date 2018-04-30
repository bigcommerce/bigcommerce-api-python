from __future__ import print_function
import bigcommerce.api
import bigcommerce.customer_login_token
import os

# Customer login tokens must be signed with an app secret loaded in the environment
os.environ['APP_CLIENT_SECRET'] = 'client secret'

# Create API object using OAuth credentials
api = bigcommerce.api.BigcommerceApi(client_id='id', store_hash='hash', access_token='token')

# Create a new customer
api.Customers.create(first_name='Bob', last_name='Johnson', email='bob.johnson@example.com')

# Or get the customer if they already exist
customer = api.Customers.all(email='bob.johnson@example.com')[0]

# Create the JWT login token
login_token = bigcommerce.customer_login_token.create(api, customer.id)

print('Token: %s' % login_token)

# You can build the URL yourself
print('%s/login/token/%s' % ('https://domain.com', login_token))

# Or use the helper method to build the URL. This uses 1 API request to get the secure domain for the store, 
# and another API request if you opt to use BC's clock for the iat.
login_token_url = bigcommerce.customer_login_token.create_url(api, customer.id, use_bc_time=True)
print('Token URL: %s' % login_token_url)
