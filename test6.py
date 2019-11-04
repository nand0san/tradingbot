#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from multiprocessing import Process, Queue
import time
import requests

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
xs = []
ys = []


def get_candles(market, tick_interval, limit=500):
    # max limit 1000, default 500
    url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tick_interval+'&limit='+str(limit)
    data = requests.get(url).json()
    return data


def parse_timestamp_price_lists(candles):
    lines = []
    for candle in candles:
        lines.append([candle[6], float(candle[4])])
    return lines


def animate(i):
    x = []
    y = []
    data = com1.get()
    print(f'Queue get: {data}')
    for point in data:
        x.append(point[0])
        y.append(point[1])
    data = []
    ax1.clear()
    ax1.plot(x, y)

def read_data():

    # init data
    market = 'BTCUSDT'
    tick_interval = '1m'

    raw_data = get_candles(market, tick_interval, limit=50)
    lines = parse_timestamp_price_lists(raw_data)
    # create a initial buffer for closed candles
    buffer = []
    for line in lines:
        current_time = time.time() * 1000
        if current_time > line[0]:
            buffer.append(line)
    print(f'Buffer inicial: {buffer}')

    while True:
        new_candles = get_candles(market, tick_interval, 2)
        new_lines = parse_timestamp_price_lists(new_candles)
        if new_lines[0][0] != buffer[-1][0]:
            print(f'Nueva vela cerrada: {new_lines[0][0]}: {new_lines[0][1]}')
            buffer.append(new_lines[0])
            buffer.pop(0)
            # comunicattor.put([new_line[0][0], new_line[1][1]])  # ponemos solo los datos nuevos
            com1.put(buffer)
        time.sleep(1)

com1 = Queue()

# # test
# market = 'BTCUSDT'
# tick_interval = '1h'
# data = get_candles(market, tick_interval)
# print(data)
# print(len(data))
# print(type(data))
#


p1 = Process(target=read_data)
p1.start()
print('Animation starting...')
ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()
