#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from binance_requests import get_candles
from datetime import datetime
from rsi_indicator import rsi


def get_closes(_candles):
    _closes = []
    for candle in _candles:
        closestr = candle[4]
        _close = float(closestr)
        _closes.append(_close)
    return _closes


def get_timestamp(_candles):
    _timestamps = []
    for candle in _candles:
        timestamp = candle[6]  # closing timestamp
        date = datetime.fromtimestamp(int(timestamp/1000))
        _timestamps.append(date)
        # _timestamps.append(timestamp)
    return _timestamps


def plot_graph(_x, _y, _market):
    plt.plot(_x, _y)
    # plt.plot(x2, y2, label='Otra')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(_market)
    plt.rc('font', size=4)
    plt.show()


def plot_rsi(_x, _y, _market='TITULO', period=14):
    _x = _x[period:]
    plt.axis([min(_x), max(_x), 0, 100])
    plot_graph(_x, _y, _market)


def plot_overlay(closes, rsi, timestamps):
    closes = closes[14:]
    timestamps = timestamps[14:]

    fig, ax1 = plt.subplots()

    color = 'tab:green'
    ax1.set_xlabel('time')
    ax1.set_ylabel('price', color=color)
    ax1.set_ylim(min(closes)-100, max(closes))
    ax1.plot(timestamps, closes, color=color, linewidth=0.5)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('rsi', color=color)  # we already handled the x-label with ax1
    ax2.set_ylim(0, 400)
    ax2.plot(timestamps, rsi, color=color,  linewidth=0.5)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.show()


# test
market = 'BTCUSDT'
interval = '5m'
rsi_interval = 14


# get data from binance_requests.py
candles = get_candles(market, interval, 1000)
closes = get_closes(candles)
timestamps = get_timestamp(candles)
time = np.array(timestamps)

# convert to numpy for rsi calculation
prices = np.array(closes)
rsi_result = rsi(prices, rsi_interval)
y = rsi_result.tolist()

# plot_rsi(timestamps, rsi_result)
# plot_overlay(timestamps, closes, timestamps, y)
plot_overlay(closes, rsi_result, time)
