import pandas_datareader.data as web
import datetime
import pandas as pd

ewma = pd.Series.ewm
start = datetime.datetime(2018, 2, 8)
end = datetime.datetime(2019, 2, 8)
stock = 'TNA'
price = web.DataReader(stock,'yahoo', start, end)
print(type(price))
n = 14

def RSI(series,n):
    delta = series.diff()
    u = delta * 0
    d = u.copy()
    i_pos = delta > 0
    i_neg = delta < 0
    u[i_pos] = delta[i_pos]
    d[i_neg] = delta[i_neg]
    rs = ewma(u, span=n).mean() / ewma(d, span=n).mean()
    return 100 - 100 / (1 + rs)

print(RSI(price.Close,n))
