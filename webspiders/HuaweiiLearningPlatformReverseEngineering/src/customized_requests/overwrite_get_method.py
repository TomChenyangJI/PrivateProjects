import os

import requests


def get_request(url, output, new_cookies="./cookies.json", jsondata=None, params=None):
    headers = {
    }

    if os.path.exists(new_cookies):
        with open(new_cookies, "r") as fi:
            import json
            cookies = json.loads(fi.read())
    else:
        cookies = {
        }
    try:
        if jsondata is not None and params is not None:
            response = requests.get(url=url, headers=headers, cookies=cookies, verify=False, json=jsondata, params=params)
        elif jsondata is not None:
            response = requests.get(url=url, headers=headers, cookies=cookies, verify=False, json=jsondata)
        elif params is not None:
            response = requests.get(url=url, headers=headers, cookies=cookies, verify=False, params=params)
        else:
            response = requests.get(url=url, headers=headers, cookies=cookies, verify=False)

    except Exception as e:
        raise e
    if output is None or output == "":
        output = "./output"
    url_component = url.strip().split("/")
    file_name = url_component[-1]
    if "." not in file_name:
        file_name = "temp.html" if file_name.strip() == "" else file_name + ".txt"

    # print("output is %s now" % output)

    os.makedirs(output, exist_ok=True)

    with open(output + "/" + file_name, "wb") as fi:
        fi.write(response.content)
    return response

#
# url = 'https://abc.xxxxxx.com/xxxxxxx/ProxyForImage/tinyimage_lts_org/v1/images/18c07bb76c2f258102dab5e1f604503a_1080x356.png'
# get_request(url, "./org.png")
