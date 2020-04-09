import pandas as pd
import requests
import csv
import datetime
import json
import hmac
import hashlib
from urllib.parse import urljoin, urlencode


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


def signatured_request(API_KEY, API_SECRET, params, endpoint, base_url, post=False, signatured=False):
    headers = {'X-MBX-APIKEY': API_KEY}
    timestamp = datetime.datetime.utcnow().timestamp()
    params['timestamp'] = int(timestamp)

    query_string = urlencode(params)
    params['signature'] = hmac.new(API_SECRET.encode('utf-8'),
                                   query_string.encode('utf-8'),
                                   hashlib.sha256).hexdigest()
    url = urljoin(base_url, endpoint)

    if not signatured:
        params.pop('timestamp', None)
        params.pop('signature', None)

    if not post:
        r = requests.get(url, headers=headers, params=params)
    else:
        r = requests.post(url, headers=headers, params=params)

    if r.status_code == 200:
        data = r.json()
        response = json.dumps(data, indent=4)
        parsed = json.loads(response)
    else:
        raise BinanceException(status_code=r.status_code, data=r.json())

    return parsed


def get_trades(API_KEY, API_SECRET, first_id=0, symbol='BTCUSDT', limit='1000'):
    base_url = 'https://api.binance.com/'
    endpoint = '/api/v3/historicalTrades?'
    params = {'symbol': symbol, 'limit': limit, 'fromId': first_id}
    trades = signatured_request(API_KEY, API_SECRET, params, endpoint, base_url)

    print(trades[-1])

    last_trade_time = trades[-1]['time']
    last_trade_id = trades[-1]['id']

    return trades, last_trade_time, last_trade_id


def get_binance_current_time():
    current_time_url = 'https://api.binance.com/api/v3/time'
    response = requests.get(current_time_url).json()
    return response['serverTime']


def get_all_trades_historical(API_KEY, API_SECRET, current_time, symbol='BTCUSDT', first_trade_id=0,
                              last_trade_time='0'):
    trades = []
    while int(last_trade_time) < int(current_time):
        i_trades, last_trade_time, last_trade_id = get_trades(API_KEY, API_SECRET, first_trade_id, symbol)
        trades = trades + i_trades
        first_trade_id = last_trade_id + 1
    return trades


def convert_to_df(trades):
    df = pd.DataFrame(trades)
    df = df.sort_values('time')
    df = df.drop_duplicates(keep='last')
    df = df.astype(float)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['time'] = df['time'].dt.tz_localize('utc').dt.tz_convert('Europe/Madrid')
    df = df.set_index('time')
    return df


if __name__ == '__main__':
    symbol = 'BTCUSDT'
    API_KEY = 'p9BRtI7CWwNt8NCSEfwHYptU07H5h2qLTfyNX6R99ODD9t39yIuBCddJeh1XKSG0'
    API_SECRET = 'drGWWSNKwDPKaxK3ts584viUkr6vYs439eaeCo2Co2mEtnlWpryYuDH7fgoOxFI3'

    current_time = get_binance_current_time()
    trades = get_all_trades_historical(API_KEY, API_SECRET, current_time, symbol)
    df = convert_to_df(trades)
    df.to_csv(f'{symbol}_historical_trades.csv', index=False, header=True, quoting=csv.QUOTE_ALL)
    print(df)
