import time
import os
from bs4 import BeautifulSoup
import requests
from config import *

def get_professions():
    res = requests.get("https://www.kickresume.com/en/help-center/resume-samples/?page=4")
    with open("temp.txt", "w") as outfi:
        outfi.write(res.text)
    with open("temp.txt", "r") as in_fi:
        content = in_fi.read()
        soup = BeautifulSoup(content, features="lxml")
        professions = soup.find_all("a", attrs={"class": "profession-dropdown-item dropdown-item"})
        profs = ""
        for pro in professions:
            if pro.text.strip() != "Any profession":
                profs += pro.text.strip() + "\n"
                # profs.append(pro.text.strip())
        with open("professions.txt", "w") as outfi:
            outfi.write(profs)


def reformat_overview(overview):
    lines = overview.split("\n")
    new_overview = ""
    for line in lines:
        line = line.strip()
        if line == "":
            new_overview += "\n"
        else:
            new_overview += line

    return new_overview.strip()


def get_pagination(res_txt):
    soup = BeautifulSoup(res_txt, features="lxml")
    nav_ele = soup.find("nav", attrs={"aria-label": "Sample pagination navigation"})
    paginations = nav_ele.find_all("a")
    max_page = ""
    for ele in paginations:
        if "1" <= ele.text <= "9999":
            max_page = ele.text
    return int(max_page)


def get_all_sample_sub_path(res_txt):
    soup = BeautifulSoup(res_txt, features="lxml")
    anchor = soup.find("div", attrs={"id": "all-samples"})
    div_tag = anchor.find("div", attrs={"class": "sample-list-grid"})
    samples = div_tag.find_all("div")
    samples_in_page = []
    # print(samples)
    for sample in samples:
        try:
            position_name = sample.find("div", attrs={"class": "sample-name"}).text
            a_tag = sample.find("a")
            href = a_tag["href"]
            cv_url = "https://www.kickresume.com" + href
            source = sample.find("source")
            cv_pdf_url = source["srcset"] # pdf url
            samples_in_page.append([position_name, cv_url, cv_pdf_url])
        except AttributeError:
            # print(">>>>>: ", sample)
            continue
    return samples_in_page


def get_overviews(res_txt):
    soup = BeautifulSoup(res_txt, features="lxml")
    li = soup.find_all("div", attrs={"class": "card card--overview white-smoke-box"})
    overviews = []
    for ele in li:
        overview_txt = reformat_overview(ele.text)
        overviews.append(overview_txt)
    return overviews


def get_overview_name(overview):
    i = overview.index("\n")
    if i > 50:
        i = overview.index(":")
    overview_name = overview[:i-1]
    return overview_name


def make_dirs_recursive(dirs):
    os.makedirs(dirs, exist_ok=True)


def save_overviews(overviews, position_name, prof):
    for overview in overviews:
        overview_name = get_overview_name(overview)
        dir_path = f"./Files/{prof}/{overview_name}"
        make_dirs_recursive(dir_path)
        with open(f"{dir_path}/{position_name}.txt", "w") as outfi:
            outfi.write(overview)


def get_text_cv(res_txt):
    soup = BeautifulSoup(res_txt, features="lxml")
    cv_content = soup.find("div", attrs={"class": "text-sample white-smoke-box p-4 mt-5"}).text
    lines = cv_content.split("\n")

    length = len(lines)
    # print(cv_content)
    modified_cv = ""
    for i in range(length):
        current_line = lines[i]
        if i >= 1:
            prev_line = lines[i - 1]
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
    return modified_cv


def get_text_cv_and_overviews(cv_url):
    res = requests.get(cv_url)
    res_txt = res.text
    modified_cv = get_text_cv(res_txt)
    overviews = get_overviews(res_txt)
    return modified_cv.strip(), overviews


def save_img_cv(pdf_url, position_name, profession):
    res = requests.get(pdf_url)
    with open(f"./Files/{profession}/img_cv/{position_name}.webp", "wb") as img_cv_out:
        img_cv_out.write(res.content)


def create_folders(prof):
    os.makedirs(f"./Files/{prof.strip()}/text_cv", exist_ok=True)
    os.makedirs(f"./Files/{prof.strip()}/img_cv", exist_ok=True)


def get_profession_resume_samples(prof="finance analyst"):
    prof = prof.strip()
    create_folders(prof)
    url = base_url + prof.replace(" ", "-").strip().lower() + "-resume-samples/"
    res = requests.get(url)
    print("\t", url)
    res_txt = res.text
    try:
        max_pages = get_pagination(res_txt)  # add sub_path, "?page=page number"
    except AttributeError:
        max_pages = 1
    # with open("prof_temp.html", "w") as out:
    #     out.write(res_txt)

    for i in range(1, max_pages + 1):
        page_url = url + f"?page={i}"
        print("\t\tPage url: ", page_url)
        page_res = requests.get(page_url)
        page_res_txt = page_res.text
        # get all sample urls
        samples_in_page = get_all_sample_sub_path(page_res_txt)
        # print(samples_in_page)
        for sample in samples_in_page:
            position_name = sample[0]  # position name
            # print(position_name)
            cv_url = sample[1]
            pdf_url = sample[2]  # pdf url
            text_cv, overviews = get_text_cv_and_overviews(cv_url)

            with open(f"./Files/{prof}/text_cv/{position_name}.txt", "w") as sample_cv_out:
                text_cv = "<#$%\n" + cv_url + "\n#$%>\n\n" + text_cv
                sample_cv_out.write(text_cv)

            pdf_url = pdf_url.replace("thumbnail", "image")
            save_img_cv(pdf_url, position_name, prof)
            save_overviews(overviews, position_name, prof)
            time.sleep(1.5)
        time.sleep(2)
