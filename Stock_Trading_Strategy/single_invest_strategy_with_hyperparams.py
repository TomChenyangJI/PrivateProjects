import json
import os
from multiprocessing import Pool, Queue, Lock, Value
import time


def get_data():
    # read data
    with open("./603119.json", "r") as fi:
        content = json.load(fi)
    return content


def get_date_close_price(entry):
    # date open close high low deal-amount deal-capital ...
    return entry[0], float(entry[2])


def get_date_open_price(entry):
    return {entry[0]: float(entry[1])}


def get_open_price_map(kline_li):
    mapping = {}
    for entry in kline_li:
        entry_dict = get_date_open_price(entry)
        mapping.update(entry_dict)

    return mapping


def convert_kline_entry_to_li(klines):
    return [e.split(',') for e in klines]


def get_multiple_day_moving_avg(li, span=5):
    length = len(li)
    # for i in range(span-1, length):
    #     val = sum(li[i+1-span:i+1])
    vals = [e[1] for e in li]

    return [
        (li[i][0], round(sum(vals[i + 1 - span:i + 1]) / span, 2))
        for i in range(span - 1, length)]


def save_result(symbol, que: Queue):
    data = []
    while not que.empty():
        val = que.get()
        data.append(val)
    base = f"./Experiment_Result/{symbol}"
    os.makedirs(base, exist_ok=True)
    ts = str(time.time())
    i = ts.find(".")
    suffix = ts[:i]
    save_path = f"{base}/result_{suffix}.json"
    with open(save_path, "w") as fo:
        json.dump(data, fo)
    print(f"\t{save_path} has been saved!")


def investing_strategy2(args):
    symbol, buy_rate, sell_rate = args
    # read data
    content = get_data()
    klines = content.get("data").get("klines")
    klines = convert_kline_entry_to_li(klines)
    open_price_map = get_open_price_map(klines)

    # moving average data
    close_prices = [get_date_close_price(entry) for entry in klines]
    mavg_5 = get_multiple_day_moving_avg(close_prices, 5)
    mavg_5 = mavg_5[5:]  # to make the two moving avergae lines to the same len
    mavg_10 = get_multiple_day_moving_avg(close_prices, 10)
    length = len(mavg_10)

    # initial capital
    capital = 50000
    amount = 0

    # strategy variables
    i = 0
    trade_times = 0
    # when previous mavg_5 price is larger than mavg_10 price, the value is True,
    # otherwise, False. the default value is None
    prev_state = True if mavg_5[i][1] > mavg_10[i][1] else False
    prev_mv_diff = abs(mavg_10[i][1] - mavg_5[i][1])
    buy = None
    sell = None
    i += 1
    open_price: float = -1.0

    while i < length:
        current_date = mavg_5[i][0]
        open_price = open_price_map.get(current_date)  # current date
        mavg_5_val = mavg_5[i][1]
        mavg_10_val = mavg_10[i][1]
        cur_abs = abs(mavg_5_val - mavg_10_val)
        if buy or sell:
            # conduct the trading action, buy or sell
            # get the price (current open price)
            if buy:
                # print("Buy Action...")
                trade_times += 1
                absolute_amount = capital // open_price
                affordable_amount = absolute_amount // 100 * 100
                commission_fee = max(affordable_amount * open_price * 0.0003, 5)
                account_transition_fee = affordable_amount * open_price * 0.00001
                note_fee = affordable_amount * open_price * 0.0005
                if capital < affordable_amount * open_price + commission_fee + account_transition_fee:
                    affordable_amount -= 100
                capital -= (affordable_amount * open_price + commission_fee + account_transition_fee)
                amount += affordable_amount

            if sell:
                # print("Sell Action...")
                trade_times += 1
                commission_fee = max(amount * open_price * 0.0003, 5)
                account_transition_fee = amount * open_price * 0.00001
                note_fee = amount * open_price * 0.0005
                capital += (
                        amount * open_price - commission_fee - account_transition_fee - note_fee)  # TODO, here I need to find how much the trading fee is
                amount = 0

            # variable maintenance
            buy = None
            sell = None
            if mavg_5_val >= mavg_10_val:
                prev_state = True
            else:  # mavg_5_val < mavg_10_val
                prev_state = False
            prev_mv_diff = cur_abs
            i += 1
            continue

        # the logic of this block is very critical
        if prev_state is True:  # mv5 >= mv10
            if mavg_5_val < mavg_10_val or (
                    mavg_5_val >= mavg_10_val and cur_abs <= prev_mv_diff and
                    ((mavg_5_val - mavg_10_val) < mavg_10_val * sell_rate)
            ):
                # time to buy the stock
                buy = True
                sell = None
        else:  # mv5 < mv10
            if mavg_5_val >= mavg_10_val or (
                    mavg_5_val < mavg_10_val and cur_abs < prev_mv_diff and
                    ((mavg_10_val - mavg_5_val) < mavg_5_val * buy_rate)
            ):
                # time to sell the stock
                sell = True
                buy = None

        if mavg_5_val >= mavg_10_val:
            prev_state = True
        else:
            prev_state = False

        prev_mv_diff = cur_abs
        i += 1
    param = {
        # buy_rate, sell_rate
        "buy_rate": buy_rate,
        "sell_rate": sell_rate,
        "profit": round(capital + amount * open_price, 2) - 50000,
        "trade_times": trade_times,
    }

    print(f"{param=}")


investing_strategy2(("603119", 0.03, 0.08))
investing_strategy2(("603119", 0.03, 0.09))

