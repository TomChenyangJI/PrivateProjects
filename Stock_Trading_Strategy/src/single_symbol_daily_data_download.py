# think about the way to collect daily data
# embed the hyperparams into the real strategy
# send reminder to myself when the moment comes

import json
import os
import requests


def get_character_hex_code_point(char: str):
    hex_code = hex(ord(char))
    hex_code = hex_code[2:]
    return "%u" + hex_code.upper()


def get_hex_code_point_of_symbol(symbol_name: str):
    base_hex_code_point = ""
    for e in symbol_name:
        char_hex_code = get_character_hex_code_point(e)
        base_hex_code_point += char_hex_code

    return base_hex_code_point


def download_daily_data(symbol: str = "603119", symbol_name: str = "浙江荣泰") -> dict:
    # get request header, cookie, params from config module
    from config import headers, cookies, params

    # update the headers, cookeis, params, such as timestamp, symbol, etc.
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

    response = requests.get('https://push2his.eastmoney.com/api/qt/stock/kline/get', params=params, cookies=cookies,
                            headers=headers)

    return response.json()


def download_data_and_save(symbol: str = "603119", symbol_name: str = "浙江荣泰", save_path="."):
    data: dict = download_daily_data(symbol, symbol_name)
    os.makedirs(save_path, exist_ok=True)
    with open(f"{save_path}/{symbol}.json", "w") as fo:
        json.dump(data, fo)
        print(f"{symbol} data has been saved to {save_path}/{symbol}.json")

# download_data_and_save()