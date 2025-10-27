from matplotlib import pyplot as plt
import os
import json
import sys 
from multiprocessing import Pool

sys.path.append("Stock_Trading_Strategy")
# from src.history_daily_data_download import *
def draw_monthly_plot(symbol, li, pic_folder=""):
    monthly_data = []
    prev_close_price = -1
    prev_date = ""
    current_mont = ""
    for ele in li:
        d = ele[0]
        price = ele[1]
        if d[:7] != current_mont:
            monthly_data.append([prev_date, prev_close_price])
            
        prev_close_price = price 
        prev_date = d 
    monthly_data.append([prev_date, prev_close_price])
    monthly_data.pop(0)
    # draw a plot 
    y = [e[0] for e in monthly_data]
    x = [e[1] for e in monthly_data]
    plt.plot(x)
    plt.ylabel("Close Price")
    plt.title(symbol)
    # os.makedirs(pic_folder, exist_ok=True)

    plt.savefig(f"{pic_folder}/{symbol}.jpg")
    plt.close()

def draw_single_symbol_plot(symbol_and_path, plot_saved_path="monthly_plots"):
    symbol, symbol_path = symbol_and_path
    try:
        with open(symbol_path) as fi:
            io = json.load(fi)
            klines = io.get("data").get("klines")
        klines = [each.split(',') for each in klines]
        close_prices = [(e[0], float(e[2]))for e in klines]
        if len(close_prices) < 1:
            return 
        draw_monthly_plot(symbol, close_prices, plot_saved_path)
    except AttributeError:
        return 

if __name__ == "__main__":
    daily_data_path = "~/daily_data"
    symbol_jsons = os.listdir(daily_data_path)
    symbol_jsons = [(each[:each.index('.')], daily_data_path + "/" + each) for each in symbol_jsons if each.endswith('json')]

    plot_saved_path = "monthly_plots"
    with Pool(20) as p:
        p.map(draw_single_symbol_plot, symbol_jsons)


# __init__.py file turn a folder into a module
# I could add __all__ = [filenames] into the __init__.py so that we can treat the file as a module
# I could add the path to envirnoment, the environment variable could be saved in ~/bash_profile as PYTHONPATH=....