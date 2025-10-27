# import modules
import sqlite3
import time

from Stock_Trading_Strategy.src.single_symbol_latest_close_price_download import single_symbol_latest_close_price_download
import pandas as pd
import numpy as np
from strategy import investing_strategy_with_hyperparams
from datetime import datetime
import datetime as dt
from multiprocessing import Pool, Queue, Lock
from News.WallStreetViews.utils import send_info_to_user

# save data to db
from Stock_Trading_Strategy.src.save_data_to_db import save_latest_data_to_db_given_res_json, db_query_for_symbol
from strategy import investing_strategy_with_hyperparams
import json
# get the data from the database of 11 records
def get_close_price_from_query(query_data: list[tuple]):
    query_data.sort(key=lambda x: x[0])
    query_data = [entry[2] for entry in query_data]
    return query_data

# check its own strategy
    # its strategy params
buy_rate: float
sell_rate: float

# check if it is needed to send an email reminder to myself


with open("Stock_Trading_Strategy/symbol_name_mapping.json") as json_obj:
    symbol_name_map = json.load(json_obj)

def get_symbol_name(symbol: str) -> str :
    return symbol_name_map.get(symbol)

def tier_based_realtime_reminder(sheet_data: list[list[str, int, int]]):

    symbol_rates_map: dict[str, list[float]] = {
                                                val[0]: [val[1], val[2]]
                                                for val in sheet_data
                                                }
    # np_arr = np.array(arr)
    # tiered_symbols = np_arr[:, 0]
    tiered_symbols = [val[0] for val in sheet_data]

    symbol_to_buy = []
    symbol_to_sell = []
    symbol_with_error = []

    for symbol in symbol_rates_map.keys():
        symbol_name = get_symbol_name(symbol)
        buy_rate, sell_rate = symbol_rates_map.get(symbol)

        # get data from db for this symbol for 11 entries
        print(symbol)
        latest_11_entries = db_query_for_symbol(symbol)
        # process data and get close price
        close_prices = get_close_price_from_query(latest_11_entries)
        # send the data_window to strategy to see if it is time to buy or sell the stock
        result: dict = investing_strategy_with_hyperparams(symbol, buy_rate, sell_rate, close_prices)
        if result.get("sell"):
            symbol_to_sell.append(symbol)
        if result.get("buy"):
            symbol_to_buy.append(symbol)
        if result.get("err"):
            symbol_with_error.append((symbol, result.get("err")))

    # sort the lists
    symbol_to_buy.sort(key=lambda x: tiered_symbols.index(x))
    symbol_to_sell.sort(key=lambda x: tiered_symbols.index(x))
    symbol_with_error.sort(key=lambda x: tiered_symbols.index(x))

    # TODO what should I do with these list objects
    # send the result notification to myself
    # set a scheduler to run the strategy
    buy_symbols = "\n".join(symbol_to_buy)
    buy_symbols = buy_symbols.strip()

    # send_info_to_user(buy_symbols, subject="Buy Symbols - " + str(datetime.fromtimestamp(time.time()).strftime("%Y/%m/%d")))

    sell_symbols = "\n".join(symbol_to_sell)
    sell_symbols = sell_symbols.strip()

    # send_info_to_user(sell_symbols,
    #           subject="Sell Symbols - " + str(datetime.fromtimestamp(time.time()).strftime("%Y/%m/%d")))

    # I may need to send the err msg to myself todo
    print(f"{symbol_to_sell=}")
    print(f"{symbol_to_buy=}")


def time_is_up(hr=6, m=0):
    delta = dt.timedelta(minutes=59)
    datetime_obj_lower_bound = dt.datetime.now() - delta
    datetime_obj_upper_bound = dt.datetime.now() + delta
    desired_time = dt.datetime.now().replace(hour=hr, minute=m)
    if datetime_obj_lower_bound < desired_time < datetime_obj_upper_bound:
        return True
    else:
        return False


if __name__ == "__main__":
    # test = single_symbol_latest_close_price_download(symbol, symbol_name)  # f43 is the close price
    # print(test)

    # two things
    # scheduler
    # while True:
    #     if time_is_up(20, 55):
    # read the tier symbols NOTE: not in a rush todo 3 remember that i have set three tiers now,check the excel file in the folder
    tier_excel = "./trading_machine_params.xlsx"
    from read_workbook import read_xlsx_book
    t1, t2, t3 = read_xlsx_book((tier_excel))
        # t1_data = np.array(pd.DataFrame(t1))
    # t1_arr = pd.DataFrame(t1).values
    # t2_arr = pd.DataFrame(t2).values
    # t3_arr = pd.DataFrame(t3).values
    # t1_map: dict[str, list[float]] = {str(int(val[0])): [float(val[1]), float(val[2])] for val in t1_arr}
    # t2_map = {str(int(val[0])): [float(val[1]), float(val[2])] for val in t2_arr}
    # t3_map = {str(int(val[0])): [float(val[1]), float(val[2])] for val in t3_arr}
    # with Pool(2) as p:
    #     p.map(tier_based_realtime_reminder, [t1, ])
    tier_based_realtime_reminder(t1)
    tier_based_realtime_reminder(t2)
    tier_based_realtime_reminder(t3)


    print("\tWaiting...")
    time.sleep(60*60)
    # way to send notification
    # send_info_to_user(subject_component="Test Mail")


# No need to read this script, it's just a copy of "main.py" file
