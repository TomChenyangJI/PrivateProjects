import pandas as pd
import os
import numpy as np
import re


def get_first_record(symbol, file):
    # symbol, file = files[0]
    try:
        excel_io = pd.ExcelFile(file)
        sheet = pd.read_excel(excel_io)
        rows, cols = sheet.shape
        data = pd.DataFrame(sheet)
        data = np.array(data)
        row = 0
        while row < rows - 1:
            entry = data[row]
            if entry[0] == 0 or entry[1] == 0:
                row += 1
            else:
                break
        record = data[row]
        first = [float(each) for each in record]
        record = [symbol] + first
        return record
    except Exception:
        return None


excel_folder = "~/PythonWorkspaces/Space1/Stock_Trading_Strategy/Experiment_Result_Excel"

files = os.listdir(excel_folder)
files = [(file[18:24], excel_folder + "/" + file) for file in files if file.endswith("xlsx")]

records = []
for entry in files:
    sym, file = entry
    record = get_first_record(sym, file)
    if record is not None:
        records.append(record)
records.sort(key=lambda x: x[2], reverse=True)

with pd.ExcelWriter("./global_maximum_profit.xlsx") as io:
    data = pd.DataFrame(records)
    data.to_excel(io)
