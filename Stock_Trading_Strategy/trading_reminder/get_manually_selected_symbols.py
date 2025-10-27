import os
import json

file_path = "filtered"


def get_symbols(p=file_path, save_path="."):
    files = os.listdir(p)
    files = [file[:file.index('.')]for file in files if file.endswith("jpg")]

    second = 'filtered'
    sec_files = os.listdir(second)
    sec_files = [file[:file.index('.')]for file in sec_files if file.endswith("jpg")] 
    files.extend(sec_files)
    files = list(set(files))
    with open(f"{save_path}/manually_selected_symbol.json", "w") as io:
        json.dump(files, io)


if __name__ == "__main__":
    get_symbols()