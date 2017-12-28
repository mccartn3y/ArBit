import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = (timestamp + request.method + request.path_url + (request.body or '')).encode('utf-8')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())
        
        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.gdax.com/'

class PlaceLimitOrder():
    
    def __init__(self, api_key, api_secret, api_pass):
             
        self.auth = CoinbaseExchangeAuth(api_key, api_secret, api_pass)

    def post_limit_order(self):
        order = '{"size": "0.01", "price": "0.100", "side": "buy", "product_id": "ETH-EUR"}'
        response = requests.post(api_url + 'orders', data=order, auth=self.auth)
        print(response)
        return response