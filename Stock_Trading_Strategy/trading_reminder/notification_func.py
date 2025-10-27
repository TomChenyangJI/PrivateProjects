import time
import requests
from datetime import datetime

url = 'https://szfilehelper.weixin.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket='
headers = {

}


def send_notification_to_wechat_filehelper(msg):
    ts = str(time.time()).replace(".", "") + "5"
    data = '{"BaseRequest":{}'
    res = requests.post(url=url, headers=headers, data=data)
    print(f"{res=}")
    if res.status_code != 200:
        print(res)
        # TODO here I may need to send an email
    # output the date and related msg shortly
    out_msg = msg[:msg.index(":")] + " has been sent."
    print(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"), msg)

