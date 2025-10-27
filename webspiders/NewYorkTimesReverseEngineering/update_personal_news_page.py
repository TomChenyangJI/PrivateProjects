from personal_page_news_update.components import *
import time
from main import customized_nyt_service
from personal_page_news_update.daily_update_nyt_to_personalpage import update_news_page


def update_daily_news(recu=0):
    if recu <= 3:
        try:
            customized_nyt_service()
            update_news_page()
            push_news_to_repo()
        except Exception as e:
            time.sleep(1)
            update_daily_news(recu+1)


if __name__ == "__main__":
    update_daily_news()
    while True:
        if time_is_up(5, 0) or time_is_up(18, 0):
            # pass
            update_daily_news()
        print("\tWaiting...")
        time.sleep(59 * 60)
