import json
import os
import time
import random
from multiprocessing import Pool
from single_symbol_daily_data_download import download_data_and_save

with open('selected_symbols.txt') as fi:
    lines = fi.readlines()
    selected_symbols = [symbol.strip() for symbol in lines if symbol != ""]


def target(param):
    global selected_symbols
    symbol, symbol_name, save_path = param
    # print(f"symbol is {symbol}")
    # todo this is where I can edit to control the symsbols to be downloaded
    # if symbol not in selected_symbols:
    #     return

    time.sleep(6 + random.randint(2, 4))
    download_data_and_save(symbol, symbol_name, save_path)


# this file is created  to download the daily data of each symbol in chinese market
if __name__ == "__main__":
    symbol_name_file = "symbol_name_mapping.json"
    with open(symbol_name_file) as fi:
        symbol_names = json.load(fi)

    save_path = "/daily_data"
    os.makedirs(save_path, exist_ok=True)

    js_files = os.listdir(save_path)
    download_json_files = [f.split(".")[0] for f in js_files if f.endswith(".json")]
    symbols = list(symbol_names.keys())
    names = list(symbol_names.values())
    save_path_li = [save_path] * len(names)
    symbol_name_pairs = list(zip(symbols, names, save_path_li))
    # symbol_name_pairs = list(filter(lambda x: (x[0] not in download_json_files), symbol_name_pairs))
    from temp_li import undownloade_symbols
    # symbol_name_pairs = list(filter(lambda x: (x[0] in undownloade_symbols), symbol_name_pairs))
    # symbol_name_pairs = list(filter(lambda x: (x[0] not in download_json_files), symbol_name_pairs))

    print(f"{len(symbol_name_pairs)=}")
    # print("sleeping....")
    # time.sleep(120*60)510100

    with Pool(4) as p:
        p.map(target, symbol_name_pairs)
    print("Done!")