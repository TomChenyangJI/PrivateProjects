import json
import os
import time
import random
from multiprocessing import Pool
from single_symbol_latest_close_price_download import *
from db_script.create_database import *


def target(param):
    symbol, symbol_name, save_path = param
    print(f"Downloading {symbol} latest data...")
    time.sleep(3 + random.randint(2, 4))
    try:
        entry: tuple = get_latest_close_price(symbol, symbol_name)
        # create table
        create_table(symbol)
        # insert the latest data to database
        insert_latest_data_into_table(symbol, entry)
    except Exception as e:
        print(e)


def target2(param):
    symbol, symbol_name, save_path, date_suffix = param
    print(f"Downloading {symbol} latest data...")
    time.sleep(3 + random.randint(2, 4))
    try:
        json_obj = single_symbol_latest_close_price_download(symbol, symbol_name)
        save_path = f"{save_path}/{date_suffix}"
        os.makedirs(save_path, exist_ok=True)
        with open(f"{save_path}/{symbol}.json", "w") as fo:
            json.dump(json_obj, fo)
    except Exception as e:
        print(e)


# this file is created  to download the daily data of each symbol in chinese market
if __name__ == "__main__":
    date_suffix = "2025-07-05"
    symbol_name_file = "symbol_name_mapping.json"
    with open(symbol_name_file) as fi:
        symbol_names = json.load(fi)
    symbols = list(symbol_names.keys())
    names = list(symbol_names.values())
    save_path = "latest_data"
    save_path_li = [save_path] * len(names)
    date_suffix_li = [date_suffix] * len(names)
    symbol_name_pairs = list(zip(symbols, names, save_path_li, date_suffix_li))
    # print("sleeping....")
    # time.sleep(120*60)
    with Pool(3) as p:
        p.map(target2, symbol_name_pairs)
# TODO, there is a problem that I may not be able to download the data successfully from one single website
# which means I may need to download the data from another data as a backup
