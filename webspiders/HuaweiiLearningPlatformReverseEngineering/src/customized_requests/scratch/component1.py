import requests

proxies = {
    'http': 'http://localhost:9090',
    'https': 'http://localhost:9090',
}

cookies = {
}

headers = {
    'Host': 'abc.xxxxxx.com',
}

response = requests.get(
    'https://abc.xxxxxx.com/xxxxxxx/ProxyForImage/tinyimage_lts_org/v1/images/6edd41eba9032d846862bf49ef01cbef_628x1280--org.png',
    cookies=cookies,
    headers=headers,
    # proxies=proxies,
    verify=False
)
with open("1.png", "wb") as fi:
    fi.write(response.content)