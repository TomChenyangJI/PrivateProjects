import sys

sys.path.append("Stock_Trading_Strategy")
import sqlite3
import time
from requests.exceptions import SSLError
from src.single_symbol_latest_close_price_download import single_symbol_latest_close_price_download
from datetime import datetime
import datetime as dt
from send_email import send_info_to_user
from strategy import investing_strategy_with_hyperparams
import json
from src.save_data_to_db import save_latest_data_to_db_given_res_json, db_query_for_symbol

# save data to db

# save_latest_data_to_db_given_res_json(symbol, json_obj)  # todo this is fine

today_date = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")


def get_close_price_from_query(query_data: list[tuple]):
    query_data.sort(key=lambda x: x[0])
    query_data = [entry[2] for entry in query_data]
    return query_data


def get_th_num(num):
    map = {
        1: "1-st",
        2: "2-nd",
        3: "3-rd"
    }
    return map.get(num, str(num) + "-th")


# check its own strategy
# its strategy params
buy_rate: float
sell_rate: float

with open(
        "Stock_Trading_Strategy/symbol_name_mapping.json") as json_obj:
    symbol_name_map = json.load(json_obj)


def get_symbol_name(symbol: str) -> str:
    return symbol_name_map.get(symbol)


def tier_based_realtime_reminder(tier_num: int, sheet_data: list[list[str, int, int]], manual_symbols: list):
    symbol_rates_map: dict[str, list[float]] = {
        val[0]: [val[1], val[2]]
        for val in sheet_data
    }

    tiered_symbols = [val[0] for val in sheet_data]

    symbol_to_buy = []
    symbol_to_sell = []
    symbol_with_error = []

    for symbol in symbol_rates_map.keys():
        if symbol not in manual_symbols:
            continue
        symbol_name = get_symbol_name(symbol)
        buy_rate, sell_rate = symbol_rates_map.get(symbol)
        # download today's data
        try:
            json_obj = single_symbol_latest_close_price_download(symbol, symbol_name)
            time.sleep(1.2)
        except TypeError:
            continue
        except SSLError:
            symbol_with_error.append(symbol)
            # print(symbol, " needs to be checked manually.")
        # save data to db
        try:
            save_latest_data_to_db_given_res_json(symbol, json_obj)
        except (sqlite3.InternalError, Exception):
            pass
        # get data from db for this symbol for 11 entries
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
            print(symbol)

    # sort the lists
    symbol_to_buy.sort(key=lambda x: tiered_symbols.index(x))
    symbol_to_sell.sort(key=lambda x: tiered_symbols.index(x))
    symbol_with_error.sort(key=lambda x: tiered_symbols.index(x))

    buy_msg = f"{today_date} {get_th_num(tier_num)} Buy Choice\n"
    if len(symbol_to_buy) != 0:
        buy_symbols = "\n".join(symbol_to_buy)
        buy_symbols = buy_symbols.strip()
        buy_msg += f"{today_date} {get_th_num(tier_num)} Buy Choice: \n" + buy_symbols
        # send_notification_to_wechat_filehelper(buy_msg)
        # send_info_to_user(buy_msg, subject=f"{today_date} {get_th_num(tier_num)} Buy Choice")
    time.sleep(0.2)

    sell_msg = f"{today_date} {get_th_num(tier_num)} Sell Choice\n"
    if len(symbol_to_sell) != 0:
        sell_symbols = "\n".join(symbol_to_sell)
        sell_symbols = sell_symbols.strip()
        sell_msg += f"{today_date} {get_th_num(tier_num)} Sell Choice: \n" + sell_symbols
        # send_notification_to_wechat_filehelper(sell_msg)
        # send_info_to_user(sell_msg, subject=f"{today_date} {get_th_num(tier_num)} Sell Choice")
    time.sleep(0.2)

    err_msg = f"{today_date} {get_th_num(tier_num)} Err Msg\n"
    if len(symbol_with_error) != 0:
        err_symbols = "\n".join(symbol_with_error).strip()
        err_msg += f"{today_date} {get_th_num(tier_num)} Error msg (manual intervene needed): \n" + err_symbols
        # send_notification_to_wechat_filehelper((err_msg))
        # send_info_to_user(err_msg, subject=f"{today_date} {get_th_num(tier_num)} Err Msg")

    # send the buy, sell, err msg together in one email
    overall_msg = buy_msg + "\n" + sell_msg + "\n" + err_msg
    send_info_to_user(overall_msg, subject=f"{today_date} - Automated Stock Trading Decision")


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

    # scheduler
    while True:
        if time_is_up(19, 30):
            # if time_is_up(23, 58):
            print(today_date, " processing the latest data ...")
            # read the tier symbols NOTE: not in a rush todo 3 remember that i have set three tiers now,check the excel file in the folder
            tier_excel = "trading_reminder/trading_machine_params.xlsx"
            from read_workbook import read_xlsx_book

            with open("trading_reminder/manually_selected_symbol.json") as fi:
                manual_symbols = json.load(fi)

            t1, t2, t3 = read_xlsx_book(tier_excel)  # t1_arr = pd.DataFrame(t1).values
            tier_based_realtime_reminder(1, t1, manual_symbols)
            tier_based_realtime_reminder(2, t2, manual_symbols)
            tier_based_realtime_reminder(3, t3, manual_symbols)

            print(today_date, " processing is done.")

        print("\tWaiting...")
        time.sleep(59 * 60)


# this is a new strategy (based on my own real experience)
#  steps
# read selected symbols
# download daily latest price
# save it do db and read previous data entries
# check if it is a good point to buy the symbol
# if yes, send notification to myself
