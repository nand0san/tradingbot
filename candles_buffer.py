import os
import json
import csv
import time
from binance_requests import get_candles as gcl


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'buffer')
CSV_FILE = 'candles.csv'


# CREATE DIRECTORY IF NOT EXISTS
try:
    os.stat(OUTPUT_DIR)
except:
    os.mkdir(OUTPUT_DIR)

# inicio archivo vacio
fieldnames = ['timestamp', 'price']
filename_path = os.path.join(OUTPUT_DIR, CSV_FILE)
with open(filename_path, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

def parse(json_data):
    parsed = json.loads(json_data)
    return parsed

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
        _timestamps.append(timestamp)
    return _timestamps

def write_line_to_csv(time, price):

    with open(filename_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([time, price])


# def get_new_candle(market, interval):

# test
market = 'BTCUSDT'
interval = '1m'
rsi_interval = 14

# get data from binance
candles = gcl(market, interval, 1000)
timestamp, price = get_timestamp(candles), get_closes(candles)
data = dict(zip(timestamp, price))

# write to csv initial data
for timestamp, price in data.items():
    write_line_to_csv(timestamp, price)

while True:
    new_candle = gcl(market, interval, 1)
    timestamp, price = get_timestamp(new_candle), get_closes(new_candle)
    new_data = dict(zip(timestamp, price))

    if timestamp[0] in list(data.keys()):
        print('Dato ya contabilizado.')
    elif not timestamp[0] in data.keys():
        print('Datos nuevos!!!!')
        write_line_to_csv(timestamp, price)

    time.sleep(1)
