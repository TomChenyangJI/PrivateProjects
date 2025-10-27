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

print(maximum)

