import json
import os
import pandas as pd
import re

def save_json_experiment_result_to_excel(base_path = f"./Experiment_Result/600285"):
    # symbol = "600285"
    result = re.findall("\d{6}", base_path)
    symbol = result[-1]
    try:
        files = os.listdir(base_path)

        experiment_result = []
        for file in files:
            if file.endswith("json"):
                with open(f"{base_path}/{file}", "r") as fi:
                    data = json.load(fi)
                    for entry in data:
                        experiment_result.append(list(entry.values()))
        head = [
            "buy_rate",
            "sell_rate",
            "profit",
            "trade_times"]
        if len(experiment_result) == 0:
            return
        experiment_result.sort(key=lambda x : x[2], reverse=True)
        folder = "./Advanced_Experiment_Result_Excel"
        os.makedirs(folder, exist_ok=True)
        excel_path = f"{folder}/experiment_result_{symbol}.xlsx"

        with pd.ExcelWriter(excel_path)as ew:
            # print(f"{experiment_result=}")
            df = pd.DataFrame(experiment_result)
            df.to_excel(ew, header=tuple(head), index=False)

        # print(f"Experiment result has been saved to excel path: {excel_path}...")
    except Exception as e:
        print(symbol, e)


if __name__ == "__main__":
    experiment_result_path = "Advanced_Experiment_Result"

    children = os.listdir(experiment_result_path)
    children = [experiment_result_path+"/"+child for child in children if os.path.isdir(experiment_result_path+"/"+child)]
    from multiprocessing import Pool
    with Pool(40) as p:
        p.map(save_json_experiment_result_to_excel, children)
    # print(children)