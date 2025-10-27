import json
import os
import time
import random
from multiprocessing import Pool
from single_symbol_latest_close_price_download import *
from db_script.create_database import *
from datetime import datetime


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


date = "20250702"
def target2(param):
    symbol, symbol_name, save_path = param
    js_files = os.listdir(save_path + "/" + date)
    download_json_files = [f.split(".")[0] for f in js_files if f.endswith(".json")]

    if symbol in download_json_files:
        return

    print(f"Downloading {symbol} latest data...")
    time.sleep(3 + random.randint(2, 4))
    try:
        json_obj = single_symbol_latest_close_price_download(symbol, symbol_name)
        save_path = f"{save_path}/{date}"
        os.makedirs(save_path, exist_ok=True)

        with open(f"{save_path}/{symbol}.json", "w") as fo:
            json.dump(json_obj, fo)
    except Exception as e:
        print(e)


# this file is created  to download the daily data of each symbol in chinese market
if __name__ == "__main__":
    symbol_name_file = "~/symbol_name_mapping.json"
    with open(symbol_name_file) as fi:
        symbol_names = json.load(fi)
    symbols = list(symbol_names.keys())
    names = list(symbol_names.values())
    save_path = "~/latest_data"
    save_path_li = [save_path] * len(names)
    symbol_name_pairs = list(zip(symbols, names, save_path_li))
    js_files = os.listdir(save_path + "/" + date)

    def check_latest_price_date(js_file, date="2025-07-03"):
        try:
            with open(js_file) as fi:
                d = json.load(fi)
                f86 = d.get('data').get('f86')
                f86 = datetime.fromtimestamp(f86).strftime('%Y-%m-%d')
                if f86 == date:
                    return True
            return False 
        except Exception:
            return False
    download_json_files = [f.split(".")[0] for f in js_files if f.endswith(".json") and check_latest_price_date(save_path + "/" + date + "/"+f)]
    symbol_name_pairs = list(filter(lambda x: (x[0] not in download_json_files), symbol_name_pairs))
    print(len(symbol_name_pairs))
    # print("sleeping....")
    # time.sleep(120*60)
    with Pool(3) as p:
        p.map(target2, symbol_name_pairs)
# TODO, there is a problem that I may not be able to download the data successfully from one single website
# which means I may need to download the data from another data as a backup
