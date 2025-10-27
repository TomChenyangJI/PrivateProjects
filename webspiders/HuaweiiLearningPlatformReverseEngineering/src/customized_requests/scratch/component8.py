import requests

proxies = {
    'http': 'http://localhost:9090',
    'https': 'http://localhost:9090',
}

cookies = {
}

headers = {
}

data = 'loginName=Mlcdr2ul2HYzMWuR93Piu&publicKeyFlag=0'

response = requests.post(
    'https://abc.xxxxxx.com/xxxxxxx/LoginWithSF',
    cookies=cookies,
    headers=headers,
    data=data,
    proxies=proxies,
)