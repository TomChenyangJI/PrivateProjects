import os

from bs4 import BeautifulSoup


with open("one_sample.html", "r") as infi:
    content = infi.read()


def get_text_cv(content):
    soup = BeautifulSoup(content, features="lxml")
    cv_content = soup.find("div", attrs={"class": "text-sample white-smoke-box p-4 mt-5"}).text
    lines = cv_content.split("\n")

    length = len(lines)
    # print(cv_content)
    modified_cv = ""
    for i in range(length):
        current_line = lines[i]
        if i >= 1:
            prev_line = lines[i-1]
            if current_line.strip() == "":
                if prev_line.strip() == "":
                    pass
                else:
                    modified_cv += "\n"
            elif current_line.startswith(" ") and prev_line.strip() != "":
                modified_cv += " " + current_line.strip()
            else:
                modified_cv += "\n" + current_line.strip()
                # print("**** manually check *****", current_line)
        else:
            modified_cv += current_line.strip()
    return modified_cv.strip()

def count_files(root_folder="./Files", txt_cv_count=0, pdf_cv_count=0, overview_count=0, all_file=0):
    subfolders = os.listdir(root_folder)

    for folder in subfolders:
        real_folder_path = os.path.join(root_folder, folder)
        if os.path.isfile(real_folder_path):
            if real_folder_path.endswith(".txt") or real_folder_path.endswith("webp"):
                all_file += 1
            if real_folder_path.endswith(".txt") and "text_cv" in \
                    real_folder_path:
                txt_cv_count += 1
            elif real_folder_path.endswith("webp"):
                pdf_cv_count += 1
            elif real_folder_path.endswith(".txt") and "position overview" in real_folder_path.lower():
                overview_count += 1
        elif os.path.isdir(real_folder_path):
            txt_cv_count, pdf_cv_count, overview_count, all_file = count_files(real_folder_path, txt_cv_count, pdf_cv_count, overview_count, all_file)
    return txt_cv_count, pdf_cv_count, overview_count, all_file


# statistics
#       txt cv  pdf cv  position overview   other overview  all files
# sample  2653,    2652,    934                   278         6517
# count = count_files()
# print(count)


