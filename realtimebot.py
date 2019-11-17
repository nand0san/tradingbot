from multiprocessing import Process
import pandas as pd
import time
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams.update({'font.size': 8})

def getNparse_candles(market='BTCUSDT', limit=100):

    # get and write init data
    orders = {}
    result = []
    url = 'https://api.binance.com/api/v3/trades?symbol=' + market + '&limit=' + str(limit) + ''
    print(url)
    init_candles = requests.get(url).json()

    for candle in init_candles:
        order_id = candle['id']
        price = float(candle['price'])
        qty = float(candle['qty'])
        timestamp = candle['time']
        my_date = datetime.fromtimestamp(timestamp / 1000)
        orders.update({order_id: [my_date, price, qty]})

    df = pd.DataFrame.from_dict(orders, orient='index', columns=['Time', 'Price', 'Qty'])
    df.to_csv('init.csv', index=False)

    while True:
        time.sleep(0.5)
        try:
            # binance request
            # on the road limit = 10
            limit = 30
            url = 'https://api.binance.com/api/v3/trades?symbol=' + market + '&limit=' + str(limit) + ''
            new_candles = requests.get(url).json()
            new_orders = {}

            for candle in new_candles:
                order_id = candle['id']
                price = float(candle['price'])
                qty = float(candle['qty'])
                timestamp = candle['time']
                my_date = datetime.fromtimestamp(timestamp / 1000)
                order = {order_id: [my_date, price, qty]}

                if not [i for i in order.keys() if i in orders.keys()]:
                    print(f'New order: {order}')

                    new_orders.update({order_id: [my_date, price, qty]})
                    ndf = pd.DataFrame.from_dict(new_orders, orient='index', columns=['Time', 'Price', 'Qty'])
                    ndf.to_csv('init.csv', mode='a', header=False, index=False)
                    orders.update({order_id: [my_date, price, qty]})

        except KeyboardInterrupt:
            print('Keyboard interrupted')
            return

def animate(i):
    plt.style.use('fivethirtyeight')
    data = pd.read_csv('init.csv')
    data['Time'] = pd.to_datetime(data['Time'])
    data.sort_values('Time', inplace=True)

    price_date = data['Time']
    price_close = data['Price']

    plt.cla()

    plt.plot_date(price_date, price_close, linestyle='solid', linewidth=0.5, marker=None)

    plt.gcf().autofmt_xdate()

    plt.title('Bitcoin Prices')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')

    plt.tight_layout()

if __name__ == '__main__':

    market = 'BTCUSDT'
    limit = 100

    # print(getNparse_candles(market, limit))

    # proceso de actualziacion cosntante en marcha
    p1 = Process(target=getNparse_candles, args=(market, limit,))
    p1.start()

    time.sleep(4)

    ani = animation.FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.show()

    p1.join()
