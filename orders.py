import time
import json
import hmac
import hashlib
import requests
from urllib.parse import urljoin, urlencode
from secret import API_KEY, API_SECRET
from log import parse, write_line_to_csv

BASE_URL = 'https://api.binance.com'
PATH = '/api/v3/order'
# PATH = '/api/v3/order/test'

headers = {'X-MBX-APIKEY': API_KEY}


class BinanceException(Exception):
    def __init__(self, status_code, data):

        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"

        super().__init__(message)


def put_order(params):

    timestamp = int(time.time() * 1000)

    if not params:
        params = {
            'symbol': 'BTCUSDT',
            'side': 'SELL',
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': 0.1,
            'price': 11500.0,
            'recvWindow': 5000,
            'timestamp': timestamp
        }

    query_string = urlencode(params)
    params['signature'] = hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    url = urljoin(BASE_URL, PATH)
    r = requests.post(url, headers=headers, params=params)

    if r.status_code == 200:
        data = r.json()
        response = json.dumps(data, indent=4)
        parsed = parse(response)
        write_line_to_csv(parsed)
    else:
        raise BinanceException(status_code=r.status_code, data=r.json())

    return r.status_code


#### test de orden
timestamp = int(time.time() * 1000)
params = {
    'symbol': 'BTCUSDT',
    'side': 'SELL',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.001,
    'price': 11500.0,
    'recvWindow': 5000,
    'timestamp': timestamp
}

response = put_order(params)
print(f'Código de respuesta de binance: {response}')
