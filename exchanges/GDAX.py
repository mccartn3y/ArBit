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

class CoinbaseManager():
    
    def __init__(self, api_key, api_secret, api_pass):
             
        self.auth = CoinbaseExchangeAuth(api_key, api_secret, api_pass)

    def get_prices(self):
        api_url = 'https://api.gdax.com/'
        r = requests.get(api_url + '/products/ETH-EUR/book?level=1', auth=self.auth)
        ask = r.json()['asks'][0][0]
        bid = r.json()['bids'][0][0]
        return {'ask': ask, 'bid': bid}
    
    def get_products(self):
        api_url = 'https://api.gdax.com/'
        r = requests.get(api_url + '/products', auth=self.auth)
        resp = [x['id'] for x in r.json()]
        return resp