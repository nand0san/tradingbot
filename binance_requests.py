import requests

# devuelve una lista de listas

def get_candles(market, tick_interval, limit=500):
    # max limit 1000, default 500
    url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tick_interval+'&limit='+str(limit)
    data = requests.get(url).json()
    return data


# # test
# market = 'BTCUSDT'
# tick_interval = '1h'
# data = get_candles(market, tick_interval)
# print(data)
# print(len(data))
# print(type(data))

