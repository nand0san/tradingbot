import matplotlib.pyplot as plt
from datetime import datetime
from binance import get_candles


def get_timestamp(candle):
    timestamp = candle[6] # closing time
    date = datetime.fromtimestamp(int(timestamp/1000))
    # date = timestamp/1000
    return date

def get_close(candle):
    closestr = candle[4]
    close = float(closestr)
    return close

def plot_graph(x, y, market):

    plt.plot(x, y)
    # plt.plot(x2, y2, label='Otra')

    plt.xlabel('Time')
    plt.ylabel('Price')

    plt.title(market)

    plt.show()


# test
market = 'BTCUSDT'
tick_interval = '1h'

candles = get_candles(market, tick_interval)

x = []
y = []
i = 0
for candle in candles:
    timestamp = get_timestamp(candle)
    x.append(timestamp)

    close = get_close(candle)
    y.append(close)

    print(x)
    print(y)

    i += 1
    if i == 5:
        break


# print(x, y)
plot_graph(x, y, market)



