#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from binance import get_candles
from datetime import datetime
from rsi_indicator import rsi


def get_closes(candles):
    closes = []
    for candle in candles:
        closestr = candle[4]
        close = float(closestr)
        closes.append(close)
    return closes


def get_timestamp(candles):
    timestamps = []
    for candle in candles:
        timestamp = candle[6]  # closing timestamp
        date = datetime.fromtimestamp(int(timestamp/1000))
        timestamps.append(date)
        # timestamps.append(timestamp)
    return timestamps


def plot_graph(x, y, market):
    plt.plot(x, y)
    # plt.plot(x2, y2, label='Otra')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(market)
    plt.rc('font', size=4)
    plt.show()


def plot_rsi(x, y, market='TITULO', period=14):
    x = x[period:]
    plot_graph(x, y, market)

def plot_stacked(x, y1, y2, market='TITULO', period=14):
    # x = x[period:]
    # y2 = y2[period:]
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle(market)
    ax1.plot(x, y1)
    ax2.plot(x, y2)

# test
market = 'BTCUSDT'
interval = '1m'
rsi_interval = 14

# get data
candles = get_candles(market, interval)
closes = get_closes(candles)
timestamps = get_timestamp(candles)

# convert to numpy for rsi calculation
prices = np.array(closes)
rsi_result = rsi(prices, rsi_interval)
# y = rsi_result.tolist()
plot_rsi(timestamps, rsi_result)
# plot_stacked(timestamps, closes, closes)
