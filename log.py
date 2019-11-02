import os
import json
import csv
import time
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'log')
CSV_FILE = 'orders.csv'


# CREATE DIRECTORY IF NOT EXISTS
try:
    os.stat(OUTPUT_DIR)
except:
    os.mkdir(OUTPUT_DIR)


def parse(json_data):
    parsed = json.loads(json_data)
    return parsed


def get_headers(parsed_line):
    headers = []
    for key in parsed_line.keys():
        headers.append(key)
    return headers


def write_line_to_csv(parsed_line):
    timestamp = int(time.time() * 1000)
    dateday = datetime.datetime.now().isoformat()
    parsed_line['timestamp'] = timestamp
    parsed_line['datetime'] = dateday
    filename_path = os.path.join(OUTPUT_DIR, CSV_FILE)
    headers = get_headers(parsed_line)

    filexists = os.path.exists(filename_path)

    with open(filename_path, "a") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
        if not filexists:
            writer.writeheader()
        writer.writerow(parsed_line)
