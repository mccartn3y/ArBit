import hmac, hashlib, time, requests, base64
import pandas as pd
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

class AskAndBidGetter():

    def get_ask_and_bid_prices(self):

        api_urls = {'GDAX': 'https://api.gdax.com/products/ETH-EUR/ticker',
            'BitStamp': 'https://www.bitstamp.net/api/v2/ticker/etheur/',
            'cex.io': 'https://cex.io/api/ticker/ETH/EUR',
            'Bitbay': 'https://bitbay.net/API/Public/ETHEUR/ticker.json',
            'Kraken': 'https://api.kraken.com/0/public/Ticker?pair=ETHEUR'}

        df = pd.read_csv('../exchanges.csv', index_col=0)

        for exchange, api_url in api_urls.items():
            if exchange != 'Kraken':
                r = requests.get(api_url)
                df.loc[exchange, 'Ask'] = r.json()['ask']
                df.loc[exchange, 'Bid'] = r.json()['bid']
            else:
                r = requests.get(api_url)
                df.loc[exchange, 'Ask'] = r.json()['result']['XETHZEUR']['a'][0]
                df.loc[exchange, 'Bid'] = r.json()['result']['XETHZEUR']['b'][0]

        df.to_csv('../exchanges.csv', encoding='utf-8')

# Unused - for reference only
class PriceManagerReference():
    
    def __init__(self, api_key, api_secret, api_pass):
             
        self.auth = CoinbaseExchangeAuth(api_key, api_secret, api_pass)

    def get_coinbase_prices(self):
        api_url = 'https://api.gdax.com/'
        r = requests.get(api_url + '/products/ETH-EUR/book?level=1', auth=self.auth)
        ask = r.json()['asks'][0][0]
        bid = r.json()['bids'][0][0]
        return {'ask': ask, 'bid': bid}
    
    def get_coinbase_products(self):
        api_url = 'https://api.gdax.com/'
        r = requests.get(api_url + '/products', auth=self.auth)
        resp = [x['id'] for x in r.json()]
        return resp