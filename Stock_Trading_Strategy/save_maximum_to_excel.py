import json
import os


base_path = "/Experiment_Result/603119"

maximum = {"profit": -1}
files = os.listdir(base_path)

for file in files:
    if file.endswith("json"):
        with open(f"{base_path}/{file}", "r") as fi:
            data = json.load(fi)
            for entry in data:
                maximum = max(entry, maximum, key=lambda x: x.get("profit"))


maximum_entries = []
head = ['buy_rate', 'sell_rate', 'profit', 'trade_times']
for file in files:
    if file.endswith("json"):
        with open(f"{base_path}/{file}", "r") as fi:
            data = json.load(fi)
            for entry in data:
                if entry.get("profit") == maximum.get("profit"):

                    maximum_entries.append(entry.values())

import pandas as pd

maximum_entries = pd.DataFrame(maximum_entries)
with pd.ExcelWriter("./maximum_profit.xlsx") as ew:
    maximum_entries.to_excel(ew, header=tuple(head))

