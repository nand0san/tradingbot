import requests

def get_candles(market, tick_interval):
    url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tick_interval
    data = requests.get(url).json()
    return data


# # test
# market = 'BTCUSDT'
# tick_interval = '1h'
# data = get_candles(market, tick_interval)
# print(data)
# print(len(data))

