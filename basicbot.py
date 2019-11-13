from multiprocessing import Process
import numpy as np
import time
import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates


def getNparse_candles(market='BTCUSDT', tick_interval='1m', limit=10):  # devuelve dos arrays numpyc con precios y time
    x = np.array([])  # time
    y = np.array([])  # precio

    while True:
        try:
            # binance request
            url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tick_interval+'&limit='+str(limit)
            candles = requests.get(url).json()

            for candle in candles:
                close_price = float(candle[4])
                close_time = candle[6]
                if close_time < (int(round(time.time() * 1000))):  # solo velas cerradas
                    x = np.append(x, close_time)
                    y = np.append(y, close_price)

            # temp_file
            np.savetxt('temp.txt', (x, y), delimiter=',')  # save to temp file
            print(f'Ciclo Ultimo precio y time: {y[-1]} {x[-1]}')
            time.sleep(3)
        except KeyboardInterrupt:
            print('Keyboard interrupted')
            return x, y  # devuelve dos numpy arrays

def animate(i):
    x, y = np.loadtxt('temp.txt', delimiter=',')

    # xLimits = [min(x), max(x)]
    # yLimits = [min(y), max(y)]
    # lineS, = ax.plot([], [], lw=2)
    # ax = plt.axes(xlim=xLimits, ylim=yLimits)
    # lineS.set_data(x, y)

    fig.autofmt_xdate()

    ntimes = mdates.num2epoch(x / 1000.0)

    plt.cla()

    ax1.plot(ntimes, y, 'r')

    # return lineS

if __name__ == '__main__':

    market = 'BTCUSDT'
    tick_interval = '1m'
    limit = 10

    # candles = get_candles(market, tick_interval, 10)
    # print(getNparse_candles())

    # proceso de actualziacion cosntante en marcha
    p1 = Process(target=getNparse_candles, args=(market, tick_interval, limit,))
    p1.start()

    # preparacion de ploteo
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ani = animation.FuncAnimation(fig, animate, interval=1000, blit=True)
    plt.show()

    # p1.join()

