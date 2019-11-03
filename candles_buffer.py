import os
import csv
import time
import requests
from multiprocessing import Queue, Process


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'buffer')
CSV_FILE = 'candles.csv'


# CREATE DIRECTORY IF NOT EXISTS
try:
    os.stat(OUTPUT_DIR)
except:
    os.mkdir(OUTPUT_DIR)

# inicio archivo vacio
fieldnames = ['Timestamp', 'Close Price']
filename_path = os.path.join(OUTPUT_DIR, CSV_FILE)
with open(filename_path, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

def get_candles(market, tick_interval, limit=500):
    # max limit 1000, default 500
    url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tick_interval+'&limit='+str(limit)
    data = requests.get(url).json()
    return data

def parse_timestamp_price_lists(candles):
    lines = []
    for candle in candles:
        lines.append([candle[6], candle[4]])
    return lines

def write_line_to_csv(line):
    with open(filename_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(line)

# test
market = 'BTCUSDT'
interval = '1m'

# get initial data from binance
candles = get_candles(market, interval, 500)
lines = parse_timestamp_price_lists(candles)

# write to csv initial data, buffer only closed candles
bufferbtc = []
for line in lines:
    current_time = time.time()*1000
    if current_time > line[0]:
        write_line_to_csv(line)
        bufferbtc.append(line)

# print(f'Current time: {time.time()*1000}')


def bufferFeed(new_value, buffer, market, interval):
    while True:
        new_candles = get_candles(market, interval, 2)
        new_lines = parse_timestamp_price_lists(new_candles)
        if new_lines[0][0] != buffer[-1][0]:
            print(f'Nueva vela cerrada: {new_lines[0][0]}: {new_lines[0][1]}')
            write_line_to_csv(new_lines[0])
            buffer.append(new_lines[0])
            buffer.pop(0)
            new_value.put(new_lines[0])
        time.sleep(1)

new_valuebtc = Queue()
# new_valueeth = Queue()
p1 = Process(target=bufferFeed, args=(new_valuebtc, bufferbtc, market, interval,))
p1.start()
# p2 = Process(target=bufferFeed, args=(new_valueeth, buffereth, 'ETHUSDT', interval,))
# p2.start()

while True:
    value = new_valuebtc.get()
    # valueeth = new_valueeth.get()
    print(value)
    # print(valueeth)
    time.sleep(0.5)
