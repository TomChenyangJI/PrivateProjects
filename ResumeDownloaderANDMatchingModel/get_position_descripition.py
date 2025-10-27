import requests
from bs4 import BeautifulSoup


# res = requests.get("https://www.kickresume.com/en/help-center/software-engineering-intern-at-agile-technologies-resume-sample-resume-sample/")
# with open("position_temp.html", "w") as outfi:
#     outfi.write(res.text)

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


with open("position_temp.html", "r") as infi:
    content = infi.read()
#
# soup = BeautifulSoup(content, features="lxml")
# li = soup.find_all("div", attrs={"class": "card card--overview white-smoke-box"})
#
# position_overview = li[0].text
# company_view = li[1].text

def get_overview(res_txt):
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


overviews = get_overview(content)
# print(get_overview(content))

for overview in overviews:
    print(get_overview_name(overview))