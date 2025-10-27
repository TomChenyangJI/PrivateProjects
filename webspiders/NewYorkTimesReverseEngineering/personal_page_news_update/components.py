from web_spider_test.NYT.config import *
import datetime


def get_daily_news_path():
    # get the html page path
    news_path = personal_page_dir + "/news/html"
    today = datetime.datetime.now()
    today_date_component = str(today.strftime("%Y/%m/%d"))
    news_path += "/" + today_date_component
    return news_path


def get_file_name(file):
    file_name = file.replace(".html", "")
    return file_name.title()


def push_news_to_repo():
    import os
    res = os.popen(
        "cd '~/GitRepos/xxx.github.io'; git status; git add .; "
        "git commit -m 'add news paper'; git push origin main;")
    print(res.read())


# design the schedule
def time_is_up(hr=6, m=0):
    delta = datetime.timedelta(minutes=59)
    datetime_obj_lower_bound = datetime.datetime.now() - delta
    datetime_obj_upper_bound = datetime.datetime.now() + delta
    desired_time = datetime.datetime.now().replace(hour=hr, minute=m)
    if datetime_obj_lower_bound < desired_time < datetime_obj_upper_bound:
        return True
    else:
        return False
