import requests
from requests.auth import AuthBase

class BitstampManager():

    def get_prices(self):
        api_url = 'https://www.bitstamp.net/api/v2/ticker/etheur/'
        r = requests.get(api_url)
        ask = r.json()['ask']
        bid = r.json()['bid']
        return {'ask': ask, 'bid': bid}