import os
import time
import shutil

parent_path = "./trained_classifier_results"


if __name__ == "__main__":
    while True:
        folders = os.listdir(parent_path)
        folders.sort()
        if len(folders) >= 2:
            print("Removing folders ... ")
            for folder in folders[:-1]:
                folder = os.path.join(parent_path, folder)
                print(f"\t{folder} removed.")
                shutil.rmtree(folder)
        print("Waiting ...")
        time.sleep(60 * 15)
