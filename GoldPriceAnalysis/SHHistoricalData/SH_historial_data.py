import requests
from config import *
import pandas as pd

params = {
    'start_date': '2025-03-10',
    'end_date': '2025-04-10',
    'inst_ids': '',
    'p': '2'
}


from datetime_obj import *
from parse_html import *
import time


if __name__ == "__main__":
    # steps
    # params
    s = -1
    e = s + 1
    current = datetime.now()
    head = None
    data = []
    flag = True
    while flag:
        try:
            s += 1
            e += 1
            end_date = get_date_params(current, s).strftime("%Y-%m-%d")
            start_date = get_date_params(current, e).strftime("%Y-%m-%d")

            if end_date < '2024-01-01':
                flag = False
                break
            p = 0
            while True:
                try:
                    p += 1
                    params['start_date'] = start_date
                    # params['start_date'] = '2025-03-10'
                    params['end_date'] = end_date
                    # params['end_date'] = '2025-04-10'
                    params['p'] = str(p)
                    response = requests.get(
                        'https://en.sge.com.cn/data/data_daily_international_new',
                        params=params,
                        cookies=cookies,
                        headers=headers,
                    )
                    print(start_date, end_date, f"{p=}")
                    data_component = get_data(response.text)
                    if p == 1 and len(data_component) == 0:
                        flag = False
                    if len(data_component) == 0:
                        break

                    data.extend(data_component)
                    if not head:
                        head = get_head(response.text)
                    time.sleep(0.5)
                except:
                    break
        except:
            break
    # request
    # get data
    head.extend(data)
    data = pd.DataFrame(head)
    data.to_excel("historical_data.xlsx")
