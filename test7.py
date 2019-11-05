import matplotlib.pyplot as plt
import matplotlib.animation as animation
# from matplotlib import style
# from multiprocessing import Process, Queue
from threading import Thread
import time
import requests
from queue import Queue
import json
import numpy as np


def grafico():
    print(f'Func Grafico:')
    x_len = 50
    y_range = [9000, 10000]

    # style.use('fivethirtyeight')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = list(range(0, 50))
    ys = [0] * x_len
    ax.set_ylim(y_range)

    # Create a blank line. We will update the line in animate
    line, = ax.plot(xs, ys)

    # Add labels
    plt.title('BTC USDT en vivo')
    plt.xlabel('Timestamp')
    plt.ylabel('Price Action')

    def animate(i, ys):

        data = np.random.random(1) * 9000

        # # if not com1.empty():
        # comunicattor = com1.get()
        # print(f'Comunicator trae: {comunicattor}')
        # data = np.array(comunicattor)
        # # # datalist = list(com1.queue)
        # # data = com1.get()
        # print(f'Queue popped data: {data} tipo {type(data)}')
        # # x.append(data)
        ys.append(data)

        ys = ys[-x_len:]

        print(f'Datos a pintar: {ys} tipos de datos: y {type(ys)}')
        line.set_ydata(ys)


        return line,

    # Set up plot to call animate() function periodically

    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,),
        interval=1000,
        blit=True)
    plt.show()


def read_data():
    parsed_price = []
    full_url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    while True:
        binanceTick1 = requests.get(full_url)
        json_response = json.loads(binanceTick1.text)

        # print(json_response, type(json_response))
        # print(json_response['price'], type(json_response))

        # timestamp = time.time() * 1000
        # print(f'Timestamp: {timestamp} {type(timestamp)}')
        price = float(json_response['price'])
        print(f'Price: {price} {type(price)} de tipo {type(price)}')

        # parsed_price = [timestamp, price]
        # print(f'Parsed Price: {parsed_price} tipo {type(parsed_price)}')
        com1.put(price)
        # print(list(com1.queue))
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':

    com1 = Queue()

    # p1 = Process(target=read_data)
    # p1.start()
    t1 = Thread(target=grafico)
    t1.start()
    read_data()
    t1.join()
