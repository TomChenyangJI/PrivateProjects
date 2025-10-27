from config import *
from utils import *


def refresh_daily_news():
    response = requests.get('https://api-one-wscn.awtmt.com/apiv1/content/information-flow',
                            params=params,
                            headers=headers)
    download_all_papers(response.json())  # and send email


if __name__ == "__main__":
    # refresh_daily_news()
    while True:
        if time_is_up(11, 20) or time_is_up(12, 50):
            refresh_daily_news()
        print("\tWaiting...")
        time.sleep(59 * 60)
