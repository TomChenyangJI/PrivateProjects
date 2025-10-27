import time
import random


url1 = "https://abc.xxxxxx.com/xxxxxxx/fg/ProxyForDownLoad/shixizhi_api/student/api/student/course/outline/application/progress/58271?all=true&filterType="


# I need to find the way to get the token or cookies.
# It's just because of the expiration of components of cookies/token.
def download_plain_text(uri=url1, output_path="test2_m3u8.json"):
    from web_spider_test.image_downloader.src import configs
    cfg = configs.__dict__
    for key, val in cfg.items():
        if key.startswith("config"):
            response = cfg.get('request_get')(
                uri, val)
            # if response.status_code == 200:
                # with open(output_path, "wb") as fi:
                #     fi.write(response.content)
                # print(f"{uri} has been downloaded!")
                # break
            print(response.text)
            time.sleep(random.randint(1, 4))


# download_plain_text()
