from multiprocessing import Process
import pandas as pd
import time
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def getNparse_candles(market='BTCUSDT', limit=100):

    # get and write init data
    orders = {}
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
    # plt.style.use('fivethirtyeight')
    data = pd.read_csv('init.csv')
    data['Time'] = pd.to_datetime(data['Time'])
    data.sort_values('Time', inplace=True)
    price_date = data['Time']
    price = data['Price']
    qty = data['Qty']

    ax1.clear()
    ax2.clear()

    ax1.plot_date(price_date, price, linestyle='solid', linewidth=0.4, color='blue', marker=None, label='Price')
    ax2.plot_date(price_date, qty, linestyle='solid', linewidth=0.4, color='red', marker=None, label='Qty')

    #Leyendas
    lines = ax1.get_lines() + ax2.get_lines()
    plt.legend(lines, [l.get_label() for l in lines], loc=2)

    # escalas
    maxprice = max(price)+20
    minprice = min(price)-20
    ax1.set_ylim(minprice, maxprice)

    maxvolume = max(qty) + 10
    ax2.set_ylim(-1, maxvolume)

    plt.gcf().autofmt_xdate()


    plt.tight_layout()

if __name__ == '__main__':

    market = 'BTCUSDT'
    limit = 1000         #  max 1000

    # print(getNparse_candles(market, limit))

    # proceso de actualziacion cosntante en marcha
    p1 = Process(target=getNparse_candles, args=(market, limit,))
    p1.start()

    time.sleep(4)

    #prepare plot
    fig = plt.figure()
    plt.rcParams.update({'font.size': 8})

    ax1 = fig.add_subplot(111)
    ax1.set_title('Date')
    ax1.set_ylabel('Price')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Qty')

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

    p1.join()
