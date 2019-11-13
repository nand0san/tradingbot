from multiprocessing import Process
import pandas as pd
import time
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mpl_dates


def getNparse_candles(market='BTCUSDT', tick_interval='1m', limit=10):

    while True:
        result = []
        time.sleep(3)
        try:
            # binance request
            url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tick_interval+'&limit='+str(limit)
            candles = requests.get(url).json()

            for candle in candles:
                close_price = float(candle[4])
                close_time = candle[6]

                if close_time < (int(round(time.time()*1000))):  # solo velas cerradas
                    my_date = datetime.fromtimestamp(close_time/1000)
                    df = pd.DataFrame([[my_date, close_price]], columns=['Time', 'Price'])
                    result.append(df)
            result = pd.concat(result)

            # temp_file
            result.to_csv('temp.csv', index=False)
            print(f'File updated {time.time()}')


        except KeyboardInterrupt:
            print('Keyboard interrupted')
            return

def animate(i):
    plt.style.use('seaborn')
    data = pd.read_csv('temp.csv')
    data['Time'] = pd.to_datetime(data['Time'])
    data.sort_values('Time', inplace=True)

    price_date = data['Time']
    price_close = data['Price']

    plt.cla()

    plt.plot_date(price_date, price_close, linestyle='solid')

    plt.gcf().autofmt_xdate()

    plt.title('Bitcoin Prices')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')

    plt.tight_layout()

if __name__ == '__main__':

    market = 'BTCUSDT'
    tick_interval = '1m'
    limit = 100

    # proceso de actualziacion cosntante en marcha
    p1 = Process(target=getNparse_candles, args=(market, tick_interval, limit,))
    p1.start()

    # preparacion de ploteo
    # fig = plt.figure()

    ani = animation.FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.show()

    p1.join()
