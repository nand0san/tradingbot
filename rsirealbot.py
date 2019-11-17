from multiprocessing import Process
import pandas as pd
import time
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from indicators import rsi
import numpy as np


def getNparse_candles(market='BTCUSDT', limit=100, period=14):

    # get and write init data
    orders = {}
    url = 'https://api.binance.com/api/v3/trades?symbol=' + market + '&limit=' + str(limit) + ''
    init_candles = requests.get(url).json()

    # get rsi
    my_rsi = rsi(np.array([float(prz['price']) for prz in init_candles]), period)
    # relleno los valores del periodo faltante para casar con la tabla
    pad = [50 for _ in range(period)]
    my_rsi = np.insert(my_rsi, 0, pad)

    for candle in init_candles:
        order_id = candle['id']
        price = float(candle['price'])
        qty = float(candle['qty'])
        timestamp = candle['time']
        rsi_index = float(my_rsi[init_candles.index(candle)])
        my_date = datetime.fromtimestamp(timestamp / 1000)
        # print({order_id: [my_date, price, qty, rsi_index]})
        orders.update({order_id: [my_date, price, qty, rsi_index]})


    df = pd.DataFrame.from_dict(orders, orient='index', columns=['Time', 'Price', 'Qty', 'RSI'])
    df.to_csv('init.csv', index=False)

    while True:
        time.sleep(0.5)
        try:
            # binance request
            limit = 15              # on the road recommended limit = 15
            url = 'https://api.binance.com/api/v3/trades?symbol=' + market + '&limit=' + str(limit) + ''
            new_candles = requests.get(url).json()
            new_orders = {}

            for candle in new_candles:
                order_id = candle['id']
                price = float(candle['price'])
                qty = float(candle['qty'])
                timestamp = candle['time']

                rsi_period_orders = [rsi_order for rsi_order in list(orders.keys())[-(period + 1):]]
                # print(rsi_period_orders, len(rsi_period_orders))

                orders_period_values = [orders[order] for order in rsi_period_orders]
                price_period_values = [order[1] for order in orders_period_values]
                # print(price_period_values, len(price_period_values))

                rsi_index = rsi(np.array(price_period_values), period)

                actual_rsi = rsi_index[0]
                # print(f'Actual RSI: {actual_rsi}')

                my_date = datetime.fromtimestamp(timestamp / 1000)
                order = {order_id: [my_date, price, qty, actual_rsi]}

                if not [i for i in order.keys() if i in orders.keys()]:
                    print(f'New order: {order}')

                    new_orders.update({order_id: [my_date, price, qty, actual_rsi]})
                    ndf = pd.DataFrame.from_dict(new_orders, orient='index', columns=['Time', 'Price', 'Qty', 'RSI'])
                    ndf.to_csv('init.csv', mode='a', header=False, index=False)
                    orders.update({order_id: [my_date, price, qty, actual_rsi]})

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
    rsi_data = data['RSI']

    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.plot_date(price_date, price, linestyle='solid', linewidth=0.4, color='blue', marker=None, label='Price')
    ax2.plot_date(price_date, qty, linestyle='solid', linewidth=0.4, color='red', marker=None, label='Qty')
    ax3.plot_date(price_date, rsi_data, linestyle='solid', linewidth=0.4, color='green', marker=None, label='RSI')

    #Leyendas
    lines = ax1.get_lines() + ax2.get_lines() + ax3.get_lines()
    plt.legend(lines, [l.get_label() for l in lines], loc=2)

    # escalas
    maxprice = max(price)
    minprice = min(price)
    ax1.set_ylim(minprice, maxprice)

    maxvolume = max(qty) + 10
    ax2.set_ylim(-1, maxvolume)
    ax3.set_yticks([0, 0.25, 0.5, 0.75, 1, 2])

    ax3.set_ylim(-50, 300)
    ax3.set_yticks([0, 25, 50, 75, 100])
    ax3.spines["right"].set_position(("axes", 1.1))

    plt.gcf().autofmt_xdate()


    plt.tight_layout()


if __name__ == '__main__':

    market = 'BTCUSDT'
    limit = 1000         #  max 1000
    rsi_period = 980

    # print(getNparse_candles(market, limit))
    # exit('pause')

    # proceso de actualziacion cosntante en marcha
    p1 = Process(target=getNparse_candles, args=(market, limit, rsi_period,))
    p1.start()

    time.sleep(4)

    #prepare plot
    fig = plt.figure()
    plt.rcParams.update({'font.size': 8})
    fig.subplots_adjust(right=0.75)  # Make some space on the right side for the extra y-axis.

    ax1 = fig.add_subplot(111)
    ax1.set_title('Date')
    ax1.set_ylabel('Price')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Qty')

    ax3 = ax1.twinx()
    ax3.set_ylabel('RSI')
    ax3.spines['right'].set_position(('axes', -0.5))

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

    p1.join()

