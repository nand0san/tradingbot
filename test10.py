import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import requests
import json
import time
import datetime


def graph(i):


    x, y = get_data()
    global x, y

    print(x, y)
    plt.plot(x, y, label='BTC/USDT')
    # plt.plot(x, y, label='quadratic')

    plt.xlabel('Time')
    plt.ylabel('Price')

    plt.title("BTC/USDT Chart")

    plt.legend()

    plt.show()


def get_data():
    global x, y

    full_url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    binanceTick1 = requests.get(full_url)
    json_response = json.loads(binanceTick1.text)
    price = float(json_response['price'])
    print(f'Price: {price} tipo {type(price)}')

    pricing = []
    timestamps = []
    pricing.append(get_data())
    timestamps.append(datetime.datetime.now().isoformat())

    x = np.array(timestamps)
    y = np.array(pricing)

    return x, y


if __name__ == '__main__':

    x = []
    y = []

    fig = plt.figure()
    ani = animation.FuncAnimation(fig, graph, interval=1000)
    plt.show()
    # while True:
    #     pricing = []
    #     timestamps = []
    #     pricing.append(get_data())
    #     timestamps.append(datetime.datetime.now().isoformat())
    #
    #     x = np.array(timestamps)
    #     y = np.array(pricing)
    #
    #     time.sleep(1)

