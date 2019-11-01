import matplotlib.pyplot as plt
from datetime import datetime
from binance import get_candles
from rsi import get_rsi


def get_timestamp(candle):
    timestamp = candle[6] # closing time
    date = datetime.fromtimestamp(int(timestamp/1000))
    # print(date)
    return date

def get_close(candle):
    closestr = candle[4]
    close = float(closestr)
    return close

def get_rsi_interval(closes, ticks):
    print(f'Rsi input len: {len(closes)}')

    # construyo intervalo
    interval = []
    rsi_result = []

    for close in closes:
        index = closes.index(close)
        if index >= ticks:
            for rsi_index in range(index - ticks, index):
                interval.append(closes[rsi_index])
            rsi_result.append(get_rsi(interval))
        else:
            rsi_result.append(50)

    print(f'Rsi output len: {len(rsi_result)}')
    return rsi_result


def plot_graph(x, y, market):

    plt.plot(x, y)
    #plt.plot(x2, y2, label='Otra')

    plt.xlabel('Time')
    plt.ylabel('Price')

    plt.title(market)

    plt.rc('font', size=4)

    plt.show()


# test
market = 'BTCUSDT'
tick_interval = '1m'
candles = get_candles(market, tick_interval)

x = []
y = []
i = 0
for candle in candles:
    timestamp = get_timestamp(candle)
    x.append(timestamp)

    close = get_close(candle)
    y.append(close)

plot_graph(x, y, market)

p = get_rsi_interval(y, 14)

plot_graph(x, p, 'RSI')





