import matplotlib.pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Process
import requests
import os
import csv
import time
from datetime import datetime
import numpy as np


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'buffer')
CSV_FILE = 'buffer.csv'

# CREATE DIRECTORY IF NOT EXISTS
try:
    os.stat(OUTPUT_DIR)
except:
    os.mkdir(OUTPUT_DIR)


def write_file(parsed_lines, headers):

    filename_path = os.path.join(OUTPUT_DIR, CSV_FILE)
    with open(filename_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        writer.writerow(headers)
        writer.writerows(parsed_lines)
    return

def write_line_to_csv(parsed_line):

    filename_path = os.path.join(OUTPUT_DIR, CSV_FILE)
    with open(filename_path, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        writer.writerow(parsed_line)
    return

def getcandles(market, tick_interval, limit=50):
    # max limit 1000, default 500
    url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tick_interval+'&limit='+str(limit)
    data = requests.get(url).json()
    print('Candles: getting...')
    return data

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

def parse_timestamp_price(candles):
    csvlines = []
    for candle in candles:
        # dateday = datetime.datetime.fromtimestamp(candle[6] / 1e3)
        dateday = datetime.fromtimestamp(int(candle[6]/1000))
        csvlines.append([dateday, float(candle[4])])
    return csvlines

def update_csv(buffer):

    while True:
        new_candles = getcandles(market, interval, 2)
        new_lines = parse_timestamp_price(new_candles)
        if new_lines[0][0] != buffer[-1][0]:
            print(f'Nueva vela cerrada: {new_lines[0][0]}: {new_lines[0][1]}')
            buffer.append(new_lines[0])
            buffer.pop(0)
            write_line_to_csv(new_lines[0])
        time.sleep(1)

def animate(i, closes, timestamps):
    plt.style.use('seaborn')

    # closes = closes[14:]
    # timestamps = timestamps[14:]

    fig, ax1 = plt.subplots()
    # plt.gcf().autofmt_xdate()
    color = 'tab:green'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price', color=color)
    ax1.set_ylim(min(closes)-100, max(closes) + 50)
    ax1.plot(timestamps, closes, color=color, linewidth=0.5)
    ax1.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped



if __name__ == '__main__':

    # get data from csv
    market = 'BTCUSDT'
    interval = '1m'
    candles = getcandles(market, interval)
    headers = ['Timestamp', 'Closing_Price']
    closes = get_closes(candles)
    timestamps = get_timestamp(candles)
    # get only closed candles
    for timestamp, close in timestamps, closes:
        current_time = time.time() * 1000
        if current_time < timestamp:
            timestamps.pop(timestamp)   # posible index error
            closes.pop(close)           # posible index error
    # convert to numpy array
    time = np.array(timestamps)
    prices = np.array(closes)


    # # write csv file with closed candles
    # write_file(buffer, headers)

    # # prepare multiprocessing
    # p1 = Process(target=update_csv, args=[buffer],)
    # # p1.start()

    # prepare animate
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
