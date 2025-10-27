from datetime import datetime
import os
import json
import re


a = 1751419994

daily_path = "20250701/"

files = os.listdir(daily_path)
files = [daily_path + "/" + file for file in files if file.endswith(".json")]

undownloaded_symbols = []
for file in files:
    with open(file) as fi:
        d = json.load(fi)
        try:
            ts = d.get("data").get("f86")
            date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            # print(date)

            if date != "2025-07-01":
                result = re.findall("\d{6}", file)
                undownloaded_symbols.append(result[1])
                # print(result[1], date)
        except AttributeError:
            continue

print(undownloaded_symbols)
print(len(undownloaded_symbols))