import json
import os
from multiprocessing import Pool, Queue, Lock, Value
import time
from threading import Thread
from threading import Lock as T_Lock
import queue as T_queue


def get_data(json_file):
    # read data
    with open(json_file, "r") as fi:
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
    vals = [e[1] for e in li]

    return [
        (li[i][0], round(sum(vals[i + 1 - span:i + 1]) / span, 2))
        for i in range(span - 1, length)]


def save_result(symbol, que: Queue):
    data = []
    while not que.empty():
        val = que.get()
        data.append(val)
    base = f"./Advanced_Experiment_Result/{symbol}"
    os.makedirs(base, exist_ok=True)
    ts = str(time.time())
    i = ts.find(".")
    suffix = ts[:i]
    save_path = f"{base}/result_{suffix}.json"
    with open(save_path, "w") as fo:
        json.dump(data, fo)
    # print(f"\t{save_path} has been saved!")


def clean_up_exception_que(que: Queue):
    data: set
    # with l:
    data = que.get()
    temp_set = set()
    que.put(temp_set)

    base = "./Advanced_Experiment_Exception_Msg"
    os.makedirs(base, exist_ok=True)
    ts = str(time.time())
    i = ts.find(".")
    suffix = ts[:i]
    save_path = f"{base}/error_msg_{suffix}.json"

    with open(save_path, "w") as fo:
        data: list = list(data)
        json.dump(data, fo)
        print(save_path)


def original_data_split(mv5, mv10):
    l = len(mv5)
    span = l // 20
    for i in range(21):
        yield mv5[i * span:], mv10[i * span:]


def investing_strategy_with_hyperparams(args):
    symbol, symbol_data_json_file, buy_rate, sell_rate = args

    content = get_data(symbol_data_json_file)
    try:
        klines = content.get("data").get("klines")
        klines = convert_kline_entry_to_li(klines)
        open_price_map = get_open_price_map(klines)

        # moving average data
        close_prices = [get_date_close_price(entry) for entry in klines]
        mavg_5 = get_multiple_day_moving_avg(close_prices, 5)
        mavg_5 = mavg_5[5:]  # to make the two moving avergae lines to the same len
        mavg_10 = get_multiple_day_moving_avg(close_prices, 10)
        length = len(mavg_10)

        t_lock = T_Lock()
        t_que = T_queue.Queue()
        temp_param = {
            # buy_rate, sell_rate
            "buy_rate": buy_rate,
            "sell_rate": sell_rate,
            "profit": float("inf"),
            "trade_times": 0,
        }
        t_que.put(temp_param)

        def sub_strategy(mavg_5, mavg_10, buy_rate, sell_rate, open_price_map):
            length = len(mavg_10)
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
                        trade_times += 1
                        commission_fee = max(amount * open_price * 0.0003, 5)
                        account_transition_fee = amount * open_price * 0.00001
                        note_fee = amount * open_price * 0.0005
                        capital += (
                                amount * open_price - commission_fee - account_transition_fee - note_fee)
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
            profit = round(capital + amount * open_price, 2) - 50000
            # if profit > 0:
            param = {
                # buy_rate, sell_rate
                "buy_rate": buy_rate,
                "sell_rate": sell_rate,
                "profit": profit,
                "trade_times": trade_times,
            }
            with t_lock:
                temp: dict = t_que.get()
                # print(temp.get("profit"), "----")
                if temp.get("profit") > profit:
                    t_que.put(param)
                else:
                    t_que.put(temp)

        threads = []
        for i in original_data_split(mavg_5, mavg_10):
            mv5, mv10 = i
            t = Thread(target=sub_strategy, args=(mv5, mv10, buy_rate, sell_rate, open_price_map))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # save the result to queue
        with l:
            param = t_que.get()
            if param.get("profit") != float("inf") and param.get("profit") > 0:
                v.value += 1
                q.put(param)
                if v.value % 500 == 0:
                    # save the values in q to file
                    save_result(symbol, q)
    except Exception as e:
        # with l:
        #     error_msg = f"{symbol} has not been conducted experiments on becuase {e} happened."
        #     temp_set: set = exception_que.get()
        #
        #     temp_set.add(error_msg)
        #     set_len = len(temp_set)
        #     exception_que.put(temp_set)
        #     if set_len != 0 and set_len % 500 == 0:
        #         clean_up_exception_que(exception_que)
        pass

# investing_strategy_with_hyperparams(("603119", 0.1, 0.2))


def param_generator(symbol, symbol_data_json_file, buy_up=50, sell_up=50):
    for buy_point in range(buy_up):
        buy_point /= 100
        for sell_point in range(sell_up):
            sell_point /= 100
            yield symbol, symbol_data_json_file, buy_point, sell_point  # todo,the trained hyperparameters


def initializer(que, lock, val, exception_q):
    global q, l, v, exception_que
    q = que
    l = lock
    v = val
    exception_que = exception_q


if __name__ == "__main__":
    symbol_name_mapping_path = "../symbol_name_mapping.json"
    with open(symbol_name_mapping_path) as fi:
        symbol_name_map = json.load(fi)
        symbols = symbol_name_map.keys()
        exception_que = Queue()
        exception_storage_temp = set()
        exception_que.put(exception_storage_temp)

        l = Lock()
        # symbols = ['601156']
        for i, symbol in enumerate(symbols):
            # symbol = "600285"
            print(f"Experiment on {symbol}...")
            symbol_data_json_file = f"{symbol}.json"

            q = Queue()
            v = Value("i", 0)
            # symbol = "600285"
            with Pool(40, initializer=initializer, initargs=(q, l, v, exception_que)) as p:
                p.map(investing_strategy_with_hyperparams, param_generator(symbol, symbol_data_json_file))
                try:
                    save_result(symbol, q)
                except Exception as e:
                    # print("main function exception: ", e)
                    pass
            q.close()
        with l:
            clean_up_exception_que(exception_que)
        exception_que.close()
