import os
import time
import uuid
import jwt


class CustomerLoginTokens(object):
    @classmethod
    def create(cls, client, id, redirect_url=None, request_ip=None, iat_time=None):
        
        # Get the client_secret needed to sign tokens from the environment
        # Intended to play nice with the Python Hello World sample app
        # https://github.com/bigcommerce/hello-world-app-python-flask
        client_secret = os.getenv('APP_CLIENT_SECRET')
        
        if not client_secret:
            raise AttributeError('No OAuth client secret specified in the environment, '
                                 'please specify an APP_CLIENT_SECRET')

        try:
            client_id = client.connection.client_id
            store_hash = client.connection.store_hash
        except AttributeError:
            raise AttributeError('Store hash or client ID not found in the connection - '
                                 'make sure an OAuth API connection is configured. Basic auth is not supported.')

        payload = dict(iss=client_id,
                       iat=int(time.time()),
                       jti=uuid.uuid4().hex,
                       operation='customer_login',
                       store_hash=store_hash,
                       customer_id=id
                       )

        if iat_time:
            payload['iat'] = iat_time

        if redirect_url:
            payload['redirect_to'] = redirect_url

        if request_ip:
            payload['request_ip'] = request_ip
        
        token = jwt.encode(payload, client_secret, algorithm='HS256')
        
        return token.decode('utf-8')

    @classmethod
    def create_url(cls, client, id, redirect_url=None, request_ip=None, use_bc_time=False):
        secure_url = client.Store.all()['secure_url']
        iat_time = None
        if use_bc_time:
            iat_time = client.Time.all()['time']
            login_token = cls.create(client, id, redirect_url, request_ip, iat_time=iat_time)
        else:
            login_token = cls.create(client, id, redirect_url, request_ip)
        return '%s/login/token/%s' % (secure_url, login_token)
