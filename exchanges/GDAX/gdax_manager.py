import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

api_url = 'https://api.gdax.com/'

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

class GetCredentialsFromFile():

    def __init__(self, filename):
        with open(filename) as f:
            for line in f:
                if "Key:" in line:
                    self.key = line.replace("Key:", "").strip()
                if "Secret:" in line:
                    self.secret = line.replace("Secret:", "").strip()
                if "Passphrase:" in line:
                    self.passphrase = line.replace("Passphrase:", "").strip()
        f.close()

class GDAXOrderManager():

    def __init__(self, filename):
        
        api_key = GetCredentialsFromFile(filename).key
        api_secret = GetCredentialsFromFile(filename).secret
        api_pass = GetCredentialsFromFile(filename).passphrase
             
        self.auth = CoinbaseExchangeAuth(api_key, api_secret, api_pass)

    def post_eth_eur_limit_order(self, size, price, side):
        order = '{{"size": "{0}", "price": "{1}", "side": "{2}", "product_id": "ETH-EUR"}}'.format(str(size), str(price), str(side))
        response = requests.post(api_url + 'orders', data=order, auth=self.auth)
        return response

    def retrieve_eth_eur_limit_orders_by_id(self, id):
        response = requests.get(api_url + 'orders/' + id, auth=self.auth)
        return response

    def cancel_eth_eur_limit_orders_by_id(self, id):
        response = requests.delete(api_url + 'orders/' + id, auth=self.auth)
        return response

    def list_all_eth_eur_orders(self):
        orders = requests.get(api_url + 'orders', auth=self.auth)
        if orders.status_code == requests.codes.ok:
            eth_eur_orders = []
            for order in orders.json():
                if order['id'] == 'ETH-EUR':
                    eth_eur_orders.append(order)
            return json.dumps(eth_eur_orders)
        else:
            print(orders.raise_for_status())
            return -1

