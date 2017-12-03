import sys
sys.path.insert(0, '/home/simon/PycharmProjects/cryptonomicon')
import sqlite3
import time
import argparse
import pdb
from src.API import *

database = '/home/simon/PycharmProjects/cryptonomicon/src/database/database.sqlite3'

def data_entry(scraped_data):

    insert_time = current_time()
    conn, cursor = connect()

    for currency, data in scraped_data.items():
        for n, item in enumerate(data):
            if n % 10 == 0:
                print("Inserting the {0}th row".format(n))
            v = item + (insert_time,) + (currency,)
            cursor.execute("INSERT INTO tokenholders (Rank, Address, Quantity, Percentage, datetime, currency)"
                           " values (?, ?, ?, ?, ?, ?)", v)
    conn.commit()
    conn.close()

def connect():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn, c

def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("currency", help="List of comma separated currencies to scrape", type=str)
    args = parser.parse_args()

    currency = args.currency.split(',')

    # Scrape data
    obj = EtherHolders(currency=currency)
    data = obj.run(sleep=1)

    data_entry(data)

if __name__ == "__main__":
    main()