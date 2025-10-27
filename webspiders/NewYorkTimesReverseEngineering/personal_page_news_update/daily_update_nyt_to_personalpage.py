from web_spider_test.NYT.config import *
from personal_page_news_update.components import *
import datetime
import os
from bs4 import BeautifulSoup

def update_news_page():
    # get the news html page
    with open(news_page_templage, "r") as infi:
        content = infi.read()

    news_path = get_daily_news_path()
    files = os.listdir(news_path)

    # get the date
    today = datetime.datetime.now()
    today_date_component = str(today.strftime("%Y/%m/%d"))

    ul_children = ""
    for file in files:
        # print(os.path.join(news_path, file))
        abs_file_path = os.path.join(news_path, file)
        # print(abs_file_path)
        audio_link = ""
        with open(abs_file_path, "r") as bs_file:
            soup = BeautifulSoup(bs_file, features="html.parser")
            audio_tag = soup.find("audio", attrs={"preload": "metadata"})
            audio_link = audio_tag['src'] if audio_tag else ""

        news_file = f"./news/html/{today_date_component}/{file}"

        news_path_tag = (f'<a class="d-flex flex-column flex-lg-row gap-3 align-items-start align-items-lg-center '
                         f'py-3 link-body-emphasis text-decoration-none border-top" href="{news_file}">')
        # get the title
        file_name = get_file_name(file)
        file_name_tag = f'<h6 class="mb-0 text-body-secondary">{file_name}</h6>'

        # date
        paper_date = f'<small class="text-body-secondary">{today_date_component}</small>'
        # full tag
        if audio_link:
            audio_ = (f'<audio controls><source src="{audio_link}" type="audio/mpeg">'
                      f'Your browser does not support the audio tag.</audio>')
            tag = f'<li>{news_path_tag}<div class="col-lg-8">{file_name_tag}{paper_date}</div></a><div>{audio_}</div></li>'
        else:
            tag = f'<li>{news_path_tag}<div class="col-lg-8">{file_name_tag}{paper_date}</div></a></li>'
        ul_children += tag

    ul_tag = f'<ul class="list-unstyled">{ul_children}</ul>'

    content = content.replace('<ul class="list-unstyled"></ul>', ul_tag)
    with open(f"{personal_page_dir}/news.html", "w") as outfi:
        outfi.write(content)


if __name__ == "__main__":
    update_news_page()
