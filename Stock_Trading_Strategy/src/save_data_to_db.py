import json
import os
import re
import time
from datetime import datetime

from src.db_script.create_database import *


def convert_raw_close_price_to_real(cp, lt):
    div = pow(10, lt)
    return cp / div


def save_history_data_to_db(
        history_data_path="daily_data"
        ):
    files = os.listdir(history_data_path)
    files = [history_data_path + "/" + file for file in files if file.endswith(".json")]

    tables = get_table_names()
    for file in files:
        result = re.findall("\d{6}", file)
        symbol = result[-1]

        if symbol in tables:
            continue

        with open(file) as fi:
            d = json.load(fi)
            try:
                klines = d.get("data").get("klines")
                entries = [entry.split(",") for entry in klines]
                entries.sort(key=lambda x: x[0], reverse=True)
                # result = re.findall("\d{6}", file)
                # symbol = result[-1]
                insert_data_into_table(symbol, entries)
                # print(result)
            except Exception as e:
                print(e)
                # pass


def save_latest_close_price_entry_to_db(latest_close_price_data_path="20250702"):
    files = os.listdir(latest_close_price_data_path)
    files = [latest_close_price_data_path + "/" + file for file in files if file.endswith(".json")]
    for file in files:
        with open(file) as fi:
            d = json.load(fi)
            try:
                result = re.findall("\d{6}", file)
                symbol = result[-1]
                close_price_raw = d.get('data').get("f43")  # close price: f43
                lt = d.get("lt")  # lt: lt-th power of 10 as the dividend
                date = datetime.fromtimestamp(d.get('data').get("f86")).strftime("%Y-%m-%d")
                open_price = convert_raw_close_price_to_real(d.get('data').get("f46"), lt)
                close_price = convert_raw_close_price_to_real(close_price_raw, lt)
                high = convert_raw_close_price_to_real(d.get('data').get("f44"), lt)
                low = convert_raw_close_price_to_real(d.get('data').get("f45"), lt)
                trade_amount = d.get('data').get("f47")
                trade_capital = d.get('data').get("f48")
                hand_change_rate = convert_raw_close_price_to_real(d.get('data').get("f168"), lt)
                entry = (date, open_price, close_price, high, low, trade_amount, trade_capital, hand_change_rate)
                # print(symbol, entry)
                insert_latest_data_into_table(symbol, entry)
            except Exception as e:
                # print(e)
                continue


def save_latest_data_to_db_given_res_json(symbol: str, d: dict):
    try:
        close_price_raw = d.get('data').get("f43")  # close price: f43
        date = datetime.fromtimestamp(d.get('data').get("f86")).strftime("%Y-%m-%d")
        open_price = convert_raw_close_price_to_real(d.get('data').get("f46"), 2)
        close_price = convert_raw_close_price_to_real(close_price_raw, 2)
        high = convert_raw_close_price_to_real(d.get('data').get("f44"), 2)
        low = convert_raw_close_price_to_real(d.get('data').get("f45"), 2)
        trade_amount = d.get('data').get("f47")
        trade_capital = d.get('data').get("f48")
        hand_change_rate = convert_raw_close_price_to_real(d.get('data').get("f168"), 2)
        entry = (date, open_price, close_price, high, low, trade_amount, trade_capital, hand_change_rate)
        insert_latest_data_into_table(symbol, entry)
    except sqlite3.IntegrityError as e:
        raise Exception(e)

if __name__ == "__main__":
    # task1 move history data into db
    history_data_path = "daily_data"
    # files = os.listdir(history_data_path)
    # files = [history_data_path + "/" + file for file in files if file.endswith(".json")]
    # for file in files:
    #     with open(file) as fi:
    #         d = json.load(fi)
    #         try:
    #             klines = d.get("data").get("klines")
    #             entries = [entry.split(",") for entry in klines]
    #             result = re.findall("\d{6}", file)
    #             symbol = result[-1]
    #             insert_data_into_table(symbol, entries)
    #             # print(result)
    #         except Exception as e:
    #             print(e)

    save_history_data_to_db(history_data_path)

    # task2 move latest price into data
    # save_latest_close_price_entry_to_db()
    pass