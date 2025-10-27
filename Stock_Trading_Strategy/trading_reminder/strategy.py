import time

from strategy_related_src.all_symbol_invest_strategy_experiment import (
    get_data,
    # get_multiple_day_moving_avg,
    save_result
)


def get_multiple_day_moving_avg(li, span=5):
    length = len(li)
    last_but_second = round(sum(li[length-span-1:length-1])/span, 2)
    last = round(sum(li[length-span:length])/span, 2)
    return last_but_second, last


def investing_strategy_with_hyperparams(symbol, buy_rate, sell_rate, close_prices) -> dict:
    # symbol, buy_rate, sell_rate, data_window = args
    # close_prices: list = data_window
    try:
        # moving average
        mavg_5 = get_multiple_day_moving_avg(close_prices, 5)  # it only contains 2 eles
        mavg_10 = get_multiple_day_moving_avg(close_prices, 10)
        # when previous mavg_5 price is larger than mavg_10 price, the value is True,
        # otherwise, False. the default value is None
        prev_state = True if mavg_5[0] >= mavg_10[0] else False
        prev_mv_diff = abs(mavg_5[0] - mavg_10[0])
        buy = None
        sell = None
        # prev_state is the state of the day before today
        mavg_5_val = mavg_5[1]
        mavg_10_val = mavg_10[1]
        cur_abs = abs(mavg_5_val - mavg_10_val)

        # the logic of this block is very critical
        if prev_state is True:  # mv5 >= mv10
            if mavg_5_val < mavg_10_val or (
                    mavg_5_val >= mavg_10_val and cur_abs <= prev_mv_diff and
                    ((mavg_5_val - mavg_10_val) < mavg_10_val * sell_rate)
            ):
                # time to buy the stock todo send notification
                buy = True
                sell = None
                return {"buy": True}
        else:  # mv5 < mv10
            if mavg_5_val >= mavg_10_val or (
                    mavg_5_val < mavg_10_val and cur_abs < prev_mv_diff and
                    ((mavg_10_val - mavg_5_val) < mavg_5_val * buy_rate)
            ):
                # time to sell the stock todo send notification
                sell = True
                buy = None
                return {"sell": True}
        return {}
    except Exception as e:
        return {"err": e}
