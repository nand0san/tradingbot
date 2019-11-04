#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from multiprocessing import Process, Queue
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def getcandles(market, tick_interval, limit=500):
    # max limit 1000, default 500
    url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tick_interval+'&limit='+str(limit)
    data = requests.get(url).json()
    print('Candles: getting...')
    return data

def parse_timestamp_price_lists(candles):
    lines = []
    for candle in candles:
        lines.append([candle[6], float(candle[4])])
    return lines


def bufferFeed(market, tick_interval, limit=50):
    print(f'Iniciando buffer...')
    # get initial data from binance
    candles = getcandles(market, tick_interval, limit)
    lines = parse_timestamp_price_lists(candles)
    # create a initial buffer for closed candles
    buffer = []
    for line in lines:
        current_time = time.time() * 1000
        if current_time > line[0]:
            buffer.append(line)
    print(f'Buffer inicial: {buffer}')
    while True:
        new_candles = getcandles(market, interval, 2)
        new_lines = parse_timestamp_price_lists(new_candles)
        if new_lines[0][0] != buffer[-1][0]:
            print(f'Nueva vela cerrada: {new_lines[0][0]}: {new_lines[0][1]}')
            buffer.append(new_lines[0])
            buffer.pop(0)
            # comunicattor.put([new_line[0][0], new_line[1][1]])  # ponemos solo los datos nuevos
            comunicattor.put(buffer)
        time.sleep(1)

def animate(i): # here frame needs to be accepted by the function since this is used in FuncAnimations
    data = comunicattor.get()  # this blocks untill it gets some data
    xdata = []
    ydata = []
    for line in data:
        xdata.append(line[0])
        ydata.append(line[1])
        # ln.set_data(xdata, ydata)
    data = []
    ax1.clear()
    ax1.plot(xdata, ydata)

    # return ln,


if __name__ == '__main__':

    plt.style.use('seaborn')
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    # # fig, ax1 = plt.subplots()
    #
    # xdata, ydata = [], []
    # ln, = plt.plot([], [])

    comunicattor = Queue()

    # init data
    market = 'BTCUSDT'
    interval = '1m'

    # # get initial data from binance
    # candles = getcandles(market, interval, 30)
    # lines = parse_timestamp_price_lists(candles)

    # # create a initial buffer for closed candles
    # buffer = []
    # for line in lines:
    #     current_time = time.time() * 1000
    #     if current_time > line[0]:
    #         buffer.append(line)

    # # get closes and timestamps from buffer
    # for line in buffer:
    #     timestamps = []
    #     closes = []
    #     timestamps.append(line[0])
    #     closes.append(line[1])

    # first, plot old values in buffer
    # color = 'tab:green'
    # ax1.set_xlabel('Date')
    # ax1.set_ylabel('Price', color=color)
    # ax1.set_ylim(min(closes)-100, max(closes) + 50)
    # ax1.plot(timestamps, closes, color=color, linewidth=0.5)
    # ax1.tick_params(axis='y', labelcolor=color)

    # start a process that get constantly new closed candles to a queue
    print('Started collecting from binance...')
    p1 = Process(target=bufferFeed, args=(market, interval,))
    p1.start()
    ani = FuncAnimation(fig, animate, blit=True, interval=1000)
    plt.show()
