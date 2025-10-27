import json
from datetime import datetime

import requests

from src.single_symbol_daily_data_download import get_hex_code_point_of_symbol

cookies = {

}

headers = {

}

params = {
    'invt': '2',
    'fltt': '1',
    'fields': 'f58,f734,f107,f57,f43,f59,f169,f301,f60,f170,f152,f177,f111,f46,f44,f45,f47,f260,f48,f261,f279,f277,f278,f288,f19,f17,f531,f15,f13,f11,f20,f18,f16,f14,f12,f39,f37,f35,f33,f31,f40,f38,f36,f34,f32,f211,f212,f213,f214,f215,f210,f209,f208,f207,f206,f161,f49,f171,f50,f86,f84,f85,f168,f108,f116,f167,f164,f162,f163,f92,f71,f117,f292,f51,f52,f191,f192,f262,f294,f295,f269,f270,f256,f257,f285,f286,f748,f747',
    'secid': '1.603119',
    # 'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
    # 'wbp2u': '|0|0|0|web',
    # 'dect': '1',
    # '_': '1751296398835',
}


# this is to get the latest daily data from the web
def single_symbol_latest_close_price_download(symbol: str = "603119", symbol_name: str = "浙江荣泰") -> dict:
    # udpate cookies, headers, params
    # cookies
    if "\\u" in symbol_name:
        hex_code = symbol_name
    else:
        hex_code = get_hex_code_point_of_symbol(symbol_name)
    cookies["HAList"] = f'ty-1-{symbol}-{hex_code}'

    # headers
    headers["Referer"] = f"https://quote.eastmoney.com/sh{symbol}.html"

    # params
    params["secid"] = f"1.{symbol}"

    response = requests.get('https://push2.eastmoney.com/api/qt/stock/get', params=params, cookies=cookies,
                            headers=headers)
    return response.json()


# till now, I have downloaded all the history data
# I have created the method to download the latest close price for certain symbol
# TODO I need to find the way to send wechat msg, or send to ji.xxx@outlook.com email
# TODO I need to design the real strategy (embed the hyperparams to remind to buy or sell)


# print(datetime.fromtimestamp(1751357506).strftime("%Y-%m-%d"))  # f86
# # close price: f43
# # lt: lt-th power of 10 as the dividend


def get_latest_close_price(symbol: str = "603119", symbol_name: str = "浙江荣泰"):
    """
    f43 close price /100
    f44 high /100
    f45 low / 100
    f46 open price / 100
    f47 trade amount
    f48 trade capital
    f168 hand change rate / 100

    """
    def convert_raw_close_price_to_real(cp, lt):
        div = pow(10, lt)
        return cp / div

    d: json = single_symbol_latest_close_price_download(symbol, symbol_name)
    # print(d)
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

    return date, open_price, close_price, high, low, trade_amount, trade_capital, hand_change_rate


# get_latest_close_price("600900", "长江电力")
# get_latest_close_price()
