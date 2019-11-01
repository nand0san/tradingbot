import pandas as pd
import numpy as np
from pandas_datareader import data as web
import matplotlib.pyplot as plt
# %matplotlib inline


def get_stock(stock, start, end):
    return web.DataReader(stock, 'iex', start, end)['Close']


def RSI(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period - 1]] = np.mean(u[:period])  # first value is sum of avg gains
    u = u.drop(u.index[:(period - 1)])
    d[d.index[period - 1]] = np.mean(d[:period])  # first value is sum of avg losses
    d = d.drop(d.index[:(period - 1)])
    rs = pd.stats.moments.ewma(u, com=period - 1, adjust=False) / \
         pd.stats.moments.ewma(d, com=period - 1, adjust=False)
    return 100 - 100 / (1 + rs)

past14Days   = [6971.73, 6937.08, 8218.05, 9251.27, 8870.82, 9114.72, 10226.86, 10107.26, 11233.95, 11767.74, 11459.71, 11104.2, 11175.87, 11429.02]

# df = pd.DataFrame(get_stock('FB', '1/1/2019', '08/31/2019'))

df = past14Days
df['RSI'] = RSI(df['Close'], 14)
df.tail()

