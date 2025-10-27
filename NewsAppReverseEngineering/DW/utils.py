import json
import requests
import time
from datetime import datetime, timedelta
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from config import *


def get_text_teaser(txt, selector=article_desc_selector):
    d = pq(txt)
    return d(selector).text()


def get_datetime_obj(d_str, default_format='%Y/%m/%d %H:%M:%S'):
    return datetime.strptime(d_str, default_format)


def get_timestamp(d_str: str, default_format='%Y/%m/%d %H:%M:%S'):
    # get time stamp from formatted str
    return datetime.strptime(d_str, default_format).timestamp()


# set current time stamp
# set start time stamp
eu_delta = timedelta(hours=18)

start_dt_obj = get_datetime_obj(datetime.now().strftime("%Y/%m/%d") + " 06:00:00")
end_dt_obj = get_datetime_obj((start_dt_obj - eu_delta).strftime("%Y/%m/%d %H:%M:%S"))

start_ts = int(start_dt_obj.timestamp() * 1000)
end_ts = int(end_dt_obj.timestamp() * 1000)


def get_content(txt):
    soup = BeautifulSoup(txt, features="html.parser")
    scripts = soup.findAll("script")
    tag_txt = scripts[-1].text.strip()
    i = tag_txt.index("{")
    dict_obj = tag_txt[i:-1]
    js_obj = json.loads(dict_obj)
    if (navi := js_obj.get("/graph-api/en/content/navigation/9097", None)) and \
            (data := navi.get("data", None)) and (content := data.get("content", None)) and \
            (contentComposition := content.get('contentComposition', None)) and \
            (informationSpaces := contentComposition.get("informationSpaces", None)) and \
            (news_obj := informationSpaces[0]) and (news := news_obj.get("news", None)) and \
            (contents := news[0].get("contents", None)):
        for content in contents:
            title = content.get("title")
            namedUrl = content.get("namedUrl")
            contentDate = content.get("contentDate")
            print(title, namedUrl, contentDate)
            # https://www.dw.com/en/malaysia-more-than-100-hurt-in-major-gas-pipeline-fire/a-72102326
            domainName = "https://www.dw.com"
            full_url = domainName + namedUrl
            cookies['_pc_st'] = str(start_ts)
            cookies['_pc_lr'] = str(end_ts)
            paper = requests.get(full_url, headers=headers, cookies=cookies)
            # with open("test.html", "w") as fi:
            #     fi.write(paper.text)
            short_desc = get_text_teaser(paper.text)  # Here is the short desc, where I also need to translate to CN
            print(short_desc)
            time.sleep(1)



def get_news_from_dw():
    cookies['_pc_st'] = str(start_ts)
    cookies['_pc_lr'] = str(end_ts)
    # response = requests.get('https://www.dw.com/de/themen/s-9077', cookies=cookies, headers=headers)
    # res = get_content(response.text)
    with open("temp.html") as fi:
        con = fi.read()
    res = get_content(con)


get_news_from_dw()
