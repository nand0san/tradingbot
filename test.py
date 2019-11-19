import requests
from indicators import rsi
import numpy as np

def get_all_rsi(market='BTCUSDT', period=14):
    # intervals 1m 5m 1h 4h 1d
    ticks = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
    # ticks_values = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    ticks_weigth = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    prices = []
    data = []
    for tick in ticks:
        url = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick + '&limit=' + str(
        period + 1)
        got_data = requests.get(url).json()
        closes = [float(close[4]) for close in got_data]
        data.append(closes)

    ticks_array = [np.array(x) for x in data]

    rsis = []
    for array in ticks_array:
        rsi_tick = rsi(array, period)
        rsis.append(rsi_tick.tolist()[0])
    print(rsis)
    average = sum(rsis) / len(rsis)
    contra_media = [x - average for x in rsis]
    print(contra_media)

    # promedio todos los rsi contra la media
    average2 = sum(contra_media) / len(contra_media)

    return contra_media[0], average2


a = get_all_rsi()
print(a)